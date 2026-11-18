using System.Globalization;
using System.Reflection;
using Newtonsoft.Json;
using questline.Model;
using questline.Server;
using Vintagestory.API.Common;

int passed = 0, failed = 0;
void Check(bool ok, string why) { if (!ok) throw new Exception(why); }
void Test(string name, Action test) {
    var culture = CultureInfo.CurrentCulture;
    var uiCulture = CultureInfo.CurrentUICulture;
    try { test(); passed++; Console.WriteLine("PASS " + name); }
    catch (Exception e) { failed++; Console.WriteLine("FAIL " + name + ": " + e.Message); }
    finally { CultureInfo.CurrentCulture = culture; CultureInfo.CurrentUICulture = uiCulture; }
}
QuestDef Q(string id, float marker) => new() { Id = id, Pos = [marker, 0], Tasks = [new() { Type = "checkbox", Count = 1 }] };
(string Domain, string Name, string Json) C(string domain, string name, string id, string extends = null, params QuestDef[] quests) =>
    (domain, name, JsonConvert.SerializeObject(new ChapterDef { Id = id, Extends = extends, Quests = quests.ToList() }));
(QuestRegistry Registry, QuestLoader Loader) Load(IEnumerable<(string Domain, string Name, string Json)> chapters,
    IEnumerable<(string Domain, string Json)> questlines = null, string working = null, HashSet<string> missingMods = null) {
    var facts = new Facts { ChapterFiles = chapters.ToList(), QuestlineFiles = questlines?.ToList() ?? [("questline", "{}")], MissingMods = missingMods ?? [] };
    var loader = new QuestLoader(facts, DispatchProxy.Create<ILogger, QuietLogger>(), working);
    return (loader.Load(), loader);
}
IEnumerable<T[]> Permutations<T>(T[] items) {
    if (items.Length == 0) { yield return []; yield break; }
    for (int i = 0; i < items.Length; i++)
        foreach (var rest in Permutations(items.Where((_, j) => i != j).ToArray())) yield return new[] { items[i] }.Concat(rest).ToArray();
}
Test("chapter discovery is ordinal and preserves in-file quest order across 24 permutations", () => {
    var files = new[] { C("z", "b", "z:b", null, Q("second", 2), Q("first", 1)), C("a", "z", "a:z", null, Q("q", 1)),
        C("a", "A", "a:A", null, Q("qA", 1)), C("a", "a", "a:a", null, Q("qa", 1)) };
    foreach (var culture in new[] { "en-US", "tr-TR" }) {
        CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo(culture);
        string snapshot = null;
        foreach (var p in Permutations(files)) {
            var (r, l) = Load(p);
            Check(string.Join(",", l.RawChapters.Keys) == "a:A,a:a,a:z,z:b", "chapter discovery follows provider/culture instead of ordinal domain + filename");
            Check(string.Join(",", r.Chapters.Last().Quests.Select(q => q.Id)) == "z:second,z:first", "in-file order changed");
            var now = r.ToJson() + string.Join("\n", l.Problems);
            snapshot ??= now; Check(snapshot == now, "registry/diagnostics changed under permutation");
        }
    }
});
Test("real loader registry order and alias winner are ordinal across cultures and permutations", () => {
    var files = new[] { "i", "I", "early" }.Select(id => {
        var chapter = new ChapterDef { Id = "shared:" + id, Order = id == "early" ? -1 : 0,
            Quests = [Q("shared:q-" + id, 1)] };
        if (id != "early") chapter.Aliases["shared:old"] = "shared:q-" + id;
        return (Domain: "questline", Name: id, Json: JsonConvert.SerializeObject(chapter));
    }).ToArray();
    var lines = new[] { "i", "I", "early" }.Select(id => ("provider" + id,
        JsonConvert.SerializeObject(new QuestlineDef { Id = "shared:" + id, Order = id == "early" ? -1 : 0 })))
        .Append(("questline", JsonConvert.SerializeObject(new QuestlineDef { Order = 1 }))).ToArray();
    // One baseline OUTSIDE the culture loop: resetting per culture misses culture-dependent state.
    string snapshot = null;
    foreach (var culture in new[] { "en-US", "tr-TR" }) {
        CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo(culture);
        CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo(culture);
        foreach (var chapters in Permutations(files)) foreach (var questlines in Permutations(lines)) {
            var (r, l) = Load(chapters, questlines);
            Check(string.Join(",", r.Chapters.Select(c => c.Id)) == "shared:early,shared:I,shared:i", "chapter order is not authored order then ordinal ID in " + culture);
            Check(string.Join(",", r.Questlines.Select(q => q.Id)) == "shared:early,shared:I,shared:i,questline:default", "questline order is not authored order then ordinal ID in " + culture);
            Check(r.Aliases["shared:old"] == "shared:q-i" && r.Find("shared:old")?.Id == "shared:q-i", "alias winner is not last ordinal chapter in " + culture);
            Check(l.Problems.Count == 0, string.Join("; ", l.Problems));
            var now = r.ToJson() + string.Join("\n", l.Problems);
            snapshot ??= now; Check(snapshot == now, "registry/diagnostics changed across cultures or permutations");
        }
    }
});
Test("questline discovery diagnostics are stable ordinal across six permutations", () => {
    var lines = new[] { ("z", "invalid"), ("a", "invalid"), ("A", "invalid") };
    foreach (var p in Permutations(lines)) {
        var (_, loader) = Load([], p);
        Check(string.Join(",", loader.Problems.Select(x => x.Split(':')[0])) == "A,a,z", "questline discovery not ordinal");
    }
});
Test("one extension replaces base in place and cross-addon IDs remain explicit", () => {
    var (r, l) = Load([C("questline", "base", "base", null, Q("q", 1), Q("tail", 2)),
        C("addon", "ext", "extension", "questline:base", Q("questline:q", 9), Q("new", 3))]);
    Check(r.Get("questline:q")?.Pos[0] == 9, "legitimate replacement lost");
    Check(string.Join(",", r.Chapters.Single().Quests.Select(q => q.Id)) == "questline:q,questline:tail,addon:new", "replacement moved or addon ID changed");
    Check(l.Problems.Count == 0, string.Join("; ", l.Problems));
});
Test("multiple replacements retain base; ambiguous additions are disabled; stable actionable diagnostics across six permutations", () => {
    var files = new[] { C("questline", "base", "base", null, Q("q", 1)),
        C("zaddon", "ext", "extension", "questline:base", Q("questline:q", 9), Q("shared:new", 3), Q("unique", 4)),
        C("aaddon", "ext", "extension", "questline:base", Q("questline:q", 8), Q("shared:new", 2)) };
    string snapshot = null;
    foreach (var p in Permutations(files)) {
        var (r, l) = Load(p);
        Check(r.Get("questline:q")?.Pos[0] == 1, "conflicting replacement did not retain base");
        Check(r.Get("shared:new") == null, "ambiguous added record not disabled");
        Check(r.Get("zaddon:unique") != null, "unrelated addition lost");
        Check(l.Problems.Count == 2, "expected exactly two conflict diagnostics");
        Check(l.Problems.All(s => s.Contains("aaddon:questline/chapters/ext.json") && s.Contains("zaddon:questline/chapters/ext.json") && s.Contains("questline:base")), "diagnostic missing target or asset paths");
        Check(l.Problems.All(s => s.Contains("Remove") || s.Contains("remove")), "diagnostic missing remediation");
        var now = r.ToJson() + string.Join("\n", l.Problems); snapshot ??= now;
        Check(snapshot == now, "conflict registry/diagnostics differ by load order");
    }
});
Test("same-file repeated extension records fail closed", () => {
    var (r, l) = Load([C("questline", "base", "base", null, Q("q", 1)),
        C("addon", "ext", "ext", "questline:base", Q("questline:q", 8), Q("questline:q", 9), Q("new", 2), Q("new", 2))]);
    Check(r.Get("questline:q")?.Pos[0] == 1 && r.Get("addon:new") == null, "same-file duplicate records were applied");
    Check(l.Problems.Count == 2, "missing same-file conflict diagnostics");
});
Test("inactive extensions cannot conflict with active replacement", () => {
    var disabled = C("a", "off", "off", "questline:base", Q("questline:q", 8));
    var obj = JsonConvert.DeserializeObject<ChapterDef>(disabled.Json); obj.RequiresMod = ["missing"]; disabled.Json = JsonConvert.SerializeObject(obj);
    var (r, l) = Load([disabled, C("questline", "base", "base", null, Q("q", 1)), C("z", "on", "on", "questline:base", Q("questline:q", 9))], missingMods: ["missing"]);
    Check(r.Get("questline:q")?.Pos[0] == 9 && l.Problems.Count == 0, "inactive extension participated");
});
Test("duplicate base chapters have stable winner and diagnostics", () => {
    var files = new[] { C("z", "z", "shared:base", null, Q("z", 2)), C("a", "a", "shared:base", null, Q("a", 1)) };
    string snapshot = null;
    foreach (var p in Permutations(files)) {
        var (r, l) = Load(p); Check(r.Get("a:a") != null && r.Get("z:z") == null, "duplicate winner not ordinal");
        var now = r.ToJson() + string.Join("\n", l.Problems); snapshot ??= now; Check(snapshot == now, "duplicate diagnostics not stable");
    }
});
Test("working copies remain authoritative and extension follows editor; domain enumeration is ordinal", () => {
    string dir = Path.Combine(Environment.GetEnvironmentVariable("TMPDIR") ?? Path.GetTempPath(), "questline-composition-" + Guid.NewGuid());
    try {
        // Deliberately create z before A/a. All three claim one ID; last ordinal working copy still wins.
        foreach (var domain in new[] { "z", "a", "A" }) {
            Directory.CreateDirectory(Path.Combine(dir, domain, "chapters"));
            File.WriteAllText(Path.Combine(dir, domain, "chapters", "base.json"), C(domain, "base", "questline:base", null, Q("questline:q", domain == "z" ? 7 : 6), Q("questline:editor", 3)).Json);
        }
        var (r, l) = Load([C("questline", "base", "base", null, Q("q", 1)), C("addon", "ext", "ext", "questline:base", Q("questline:q", 9))], working: dir);
        Check(r.Get("questline:q")?.Pos[0] == 9 && r.Get("questline:editor") != null, "editor/extension precedence changed");
        Check(JsonConvert.DeserializeObject<ChapterDef>(l.RawChapters["questline:base"]).Quests[0].Pos[0] == 7, "working domain ordering is not ordinal");
        Check(l.Edited.Contains("questline:base"), "edited marker lost");
        var conflicted = Load([C("questline", "base", "base", null, Q("q", 1)),
            C("addon", "ext", "ext", "questline:base", Q("questline:q", 9)),
            C("other", "ext", "ext", "questline:base", Q("questline:q", 8))], working: dir);
        Check(conflicted.Registry.Get("questline:q")?.Pos[0] == 7, "conflict did not retain authoritative editor record");
    } finally { if (Directory.Exists(dir)) Directory.Delete(dir, true); }
});
Test("extension art survives blocked quest conflicts in ordinal file and authored art order", () => {
    (string Domain, string Name, string Json) WithArt((string Domain, string Name, string Json) file, params string[] labels) {
        var chapter = JsonConvert.DeserializeObject<ChapterDef>(file.Json);
        chapter.Art = labels.Select(label => new ArtDef { Type = "text", Text = label, Pos = [3, 4], Scale = 2, Color = "#123456" }).ToList();
        return (file.Domain, file.Name, JsonConvert.SerializeObject(chapter));
    }
    var files = new[] {
        WithArt(C("questline", "base", "base", null, Q("q", 1)), "base"),
        WithArt(C("addon", "z", "z", "questline:base", Q("questline:q", 9)), "z-first", "z-second"),
        WithArt(C("addon", "A", "A", "questline:base", Q("questline:q", 8)), "A-first", "A-second") };
    foreach (var p in Permutations(files)) {
        var (r, l) = Load(p);
        Check(r.Get("questline:q")?.Pos[0] == 1 && l.Problems.Count == 1, "fixture must retain base after conflict");
        var art = r.Chapters.Single().Art;
        Check(string.Join(",", art.Select(a => a.Text)) == "questline:base,addon:A-first,addon:A-second,addon:z-first,addon:z-second", "base/extension art lost or reordered with blocked records");
        Check(art.All(a => a.Type == "text" && a.Pos.SequenceEqual(new float[] { 3, 4 }) && a.Scale == 2 && a.Color == "#123456"), "art payload changed");
    }
});
Test("same-domain working filenames use last ordinal winner regardless of creation order and culture", () => {
    string snapshot = null;
    foreach (var culture in new[] { "en-US", "tr-TR" }) foreach (var names in Permutations(new[] { "i", "I" })) {
        CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo(culture);
        CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo(culture);
        string dir = Path.Combine(Environment.GetEnvironmentVariable("TMPDIR") ?? Path.GetTempPath(), "questline-working-" + Guid.NewGuid());
        try {
            var chapters = Path.Combine(dir, "questline", "chapters"); Directory.CreateDirectory(chapters);
            foreach (var name in names) File.WriteAllText(Path.Combine(chapters, name + ".json"), C("questline", name, "base", null, Q("q", name == "i" ? 7 : 6)).Json);
            var (r, l) = Load([C("questline", "base", "base", null, Q("q", 1))], working: dir);
            Check(r.Get("questline:q")?.Pos[0] == 7, "last ordinal working filename did not win in " + culture);
            Check(JsonConvert.DeserializeObject<ChapterDef>(l.RawChapters["questline:base"]).Quests.Single().Pos[0] == 7 && l.Edited.Contains("questline:base"), "raw/editor state does not reflect winning file");
            Check(l.Problems.Count == 0, string.Join("; ", l.Problems));
            var now = r.ToJson(); snapshot ??= now; Check(snapshot == now, "working registry changed with creation order or culture");
        } finally { if (Directory.Exists(dir)) Directory.Delete(dir, true); }
    }
});
Test("all 16 shipped base-to-extension replacements survive shuffled real content composition", () => {
    string root = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "../../../../../"));
    var files = Directory.GetFiles(Path.Combine(root, "content"), "*.json", SearchOption.AllDirectories)
        .Where(f => f.Replace('\\', '/').Contains("/questline/chapters/"))
        .Select(f => (Domain: new DirectoryInfo(Path.GetDirectoryName(f)).Parent.Parent.Name, Name: Path.GetFileNameWithoutExtension(f), Json: File.ReadAllText(f))).ToArray();
    Check(files.Length == 56, $"expected 56 extracted content files, got {files.Length}");
    var baseline = Load(files);
    var qualified = files.Select(f => {
        var c = JsonConvert.DeserializeObject<ChapterDef>(f.Json);
        typeof(QuestLoader).GetMethod("Qualify", BindingFlags.NonPublic | BindingFlags.Instance).Invoke(baseline.Loader, [c, f.Domain, f.Name]);
        if (c.Extends != null && !c.Extends.Contains(':')) c.Extends = f.Domain + ":" + c.Extends;
        return c;
    }).ToArray();
    var bases = qualified.Where(c => c.Extends == null).ToDictionary(c => c.Id);
    var replacements = qualified.Where(c => c.Extends != null).SelectMany(c => c.Quests
        .Where(q => bases[c.Extends].Quests.Any(b => b.Id == q.Id))).ToArray();
    Check(replacements.Length == 16, $"expected 16 intentional replacements, got {replacements.Length}");
    Check(!baseline.Loader.Problems.Any(p => p.Contains("ambiguous extension")), "shipped content has composition conflicts");
    foreach (var q in replacements) {
        var actual = baseline.Registry.Get(q.Id);
        Check(actual != null, "lost shipped replacement " + q.Id);
        // Payout normalization belongs to a separate contract; compare teaching mechanics here.
        Check(JsonConvert.SerializeObject(actual.Tasks) == JsonConvert.SerializeObject(q.Tasks), "replacement mechanics changed: " + q.Id);
        Check(JsonConvert.SerializeObject(actual.Page) == JsonConvert.SerializeObject(q.Page), "replacement prose changed: " + q.Id);
        Check(JsonConvert.SerializeObject(actual.Requires) == JsonConvert.SerializeObject(q.Requires), "replacement prerequisites changed: " + q.Id);
    }
    string snapshot = baseline.Registry.ToJson() + string.Join("\n", baseline.Loader.Problems);
    foreach (int seed in Enumerable.Range(0, 12)) {
        var rng = new Random(seed); var p = files.OrderBy(_ => rng.Next()).ToArray(); var loaded = Load(p);
        Check(snapshot == loaded.Registry.ToJson() + string.Join("\n", loaded.Loader.Problems), "shipped registry/diagnostics changed under seed " + seed);
    }
});
Console.WriteLine($"Composition: {passed} passed, {failed} failed");
return failed == 0 ? 0 : 1;

public class QuietLogger : DispatchProxy {
    protected override object Invoke(MethodInfo method, object[] args) => method.ReturnType == typeof(void) ? null : method.ReturnType.IsValueType ? Activator.CreateInstance(method.ReturnType) : null;
}
public class Facts : IGameFacts {
    public List<(string Domain, string Name, string Json)> ChapterFiles = [];
    public List<(string Domain, string Json)> QuestlineFiles = [];
    public HashSet<string> MissingMods = [];
    public IEnumerable<(string Domain, string Name, string Json)> Chapters() => ChapterFiles;
    public IEnumerable<(string Domain, string Json)> Questlines() => QuestlineFiles;
    public bool IsModLoaded(string id) => !MissingMods.Contains(id);
    public bool CollectibleExists(string code) => true;
    public bool AnyMatches(string kind, string pattern) => true;
    public bool HasLang(string key) => true;
    public byte[] Texture(string location) => null;
}
