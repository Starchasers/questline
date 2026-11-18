using System.Diagnostics;
using System.Globalization;
using System.Reflection;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using questline.Model;
using questline.Server;
using Vintagestory.API.Common;

string root = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "../../../../../"));
string output = Path.Combine(Environment.GetEnvironmentVariable("TMPDIR") ?? Path.GetTempPath(), "aog-corpus-" + Guid.NewGuid() + ".json");
int passed = 0;
var originalCulture = CultureInfo.CurrentCulture;
var originalUiCulture = CultureInfo.CurrentUICulture;
void Check(bool ok, string why) { if (!ok) throw new Exception(why); }
string Signature(QuestDef q, bool ignoreRewards = true) {
    // Loader normalizes material payouts independently of curriculum composition.
    var j = JObject.FromObject(q);
    if (ignoreRewards) { j.Remove("rewards"); j.Remove("Rewards"); }
    return j.ToString(Formatting.None);
}
(QuestRegistry Registry, QuestLoader Loader) Load(JToken corpus, int seed) {
    var rng = new Random(seed);
    var facts = new Facts {
        Mods = corpus["mods"].Values<string>().ToHashSet(),
        Files = corpus["chapters"].OrderBy(_ => rng.Next()).Select(x => ((string)x["domain"], (string)x["name"], (string)x["json"])).ToList()
    };
    var loader = new QuestLoader(facts, DispatchProxy.Create<ILogger, QuietLogger>());
    return (loader.Load(), loader);
}
try {
    var process = new ProcessStartInfo("python3") { WorkingDirectory = root, UseShellExecute = false };
    process.ArgumentList.Add("verification/artofgrowing/check.py"); process.ArgumentList.Add("--emit"); process.ArgumentList.Add(output);
    using (var p = Process.Start(process)) { p.WaitForExit(); Check(p.ExitCode == 0, "shipped patch/coverage validation failed"); }
    var scenarios = JArray.Parse(File.ReadAllText(output));
    foreach (var scenario in scenarios) {
        string name = (string)scenario["name"];
        var baseline = Load(scenario["baseline"], 0);
        var active = scenario["active"];
        var changed = active["edits"].Select(e => "questline:" + (string)e[1]).ToHashSet();
        string snapshot = null;
        foreach (string culture in new[] { "en-US", "tr-TR" }) foreach (int seed in Enumerable.Range(0, 4)) {
            CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo(culture);
            CultureInfo.CurrentUICulture = CultureInfo.GetCultureInfo(culture);
            var loaded = Load(active, seed);
            // ALL prerequisites, not merely references to newly added AoG records.
            foreach (var q in loaded.Registry.Quests.Values) {
                foreach (var prerequisite in q.Requires?.QuestIds() ?? Enumerable.Empty<string>())
                    Check(loaded.Registry.Get(prerequisite) != null, name + ": dangling prerequisite " + q.Id + " -> " + prerequisite);
            }
            Check(!loaded.Loader.Problems.Any(p => p.Contains("ambiguous extension") || p.Contains("defined twice") || p.Contains("quest disabled") || p.Contains("can never unlock") || p.Contains("which no questline has")), name + ": " + string.Join("; ", loaded.Loader.Problems));
            Check(!loaded.Loader.Problems.Except(baseline.Loader.Problems).Any(), name + ": new loader diagnostics: " + string.Join("; ", loaded.Loader.Problems.Except(baseline.Loader.Problems)));
            foreach (var chapter in active["chapters"].Where(c => (string)c["domain"] == "questlineartofgrowing")) {
                var extension = JsonConvert.DeserializeObject<ChapterDef>((string)chapter["json"]);
                var mods = active["mods"].Values<string>().ToHashSet();
                if (extension.RequiresMod.Any(mod => !mods.Contains(mod))) continue;
                typeof(QuestLoader).GetMethod("Qualify", BindingFlags.NonPublic | BindingFlags.Instance).Invoke(loaded.Loader, [extension, "questlineartofgrowing", (string)chapter["name"]]);
                foreach (var stage in extension.Quests) {
                    var actual = loaded.Registry.Get(stage.Id);
                    Check(actual != null, name + ": missing additive stage " + stage.Id);
                    Check(Signature(actual) == Signature(stage), name + ": additive stage changed " + stage.Id);
                }
            }
            foreach (var q in baseline.Registry.Quests.Values) {
                var actual = loaded.Registry.Get(q.Id);
                Check(actual != null, name + ": original ID lost " + q.Id);
                if (!changed.Contains(q.Id)) Check(Signature(actual, false) == Signature(q, false), name + ": unaffected content changed " + q.Id);
            }
            // Each applied source-record replacement must survive real extension merging.
            // Compare against a loader-qualified replacement, not unqualified raw JSON.
            foreach (var e in active["edits"]) {
                string id = "questline:" + (string)e[1];
                var source = active["chapters"].First(c => (string)c["domain"] == "questline" && (string)c["name"] == Path.GetFileNameWithoutExtension((string)e[0]));
                var expectedChapter = JsonConvert.DeserializeObject<ChapterDef>((string)source["json"]);
                typeof(QuestLoader).GetMethod("Qualify", BindingFlags.NonPublic | BindingFlags.Instance).Invoke(loaded.Loader, [expectedChapter, "questline", (string)source["name"]]);
                var expected = expectedChapter.Quests.Single(q => q.Id == id);
                // Other optional packs may intentionally override a vanilla source record.
                // The corresponding affected optional source record must then be patched too.
                bool superseded = active["chapters"].Any(c => {
                    var d = JsonConvert.DeserializeObject<ChapterDef>((string)c["json"]);
                    return d.Extends == expectedChapter.Id.Replace("questline:", "") && d.Quests.Any(q => q.Id == id.Replace("questline:", ""));
                });
                if (!superseded) Check(Signature(loaded.Registry.Get(id)) == Signature(expected), name + ": patched mechanics/prose/prerequisites lost " + id);
            }
            if (changed.Count == 0) Check(baseline.Registry.ToJson() == loaded.Registry.ToJson(), name + ": inactive addon changed the registry");
            var now = loaded.Registry.ToJson() + string.Join("\n", loaded.Loader.Problems);
            snapshot ??= now; Check(snapshot == now, name + ": nondeterministic composition");
        }
        passed++; Console.WriteLine("PASS " + name + " (all prerequisites, retained content, patches, 8 shuffled/culture loads)");
    }
    Console.WriteLine($"Art of Growing: {passed} scenarios passed; native gameplay NOT run");
    return 0;
} catch (Exception e) { Console.Error.WriteLine("FAIL Art of Growing: " + e); return 1; }
finally {
    CultureInfo.CurrentCulture = originalCulture;
    CultureInfo.CurrentUICulture = originalUiCulture;
    if (File.Exists(output)) File.Delete(output);
}

public class QuietLogger : DispatchProxy {
    protected override object Invoke(MethodInfo method, object[] args) => method.ReturnType == typeof(void) ? null : method.ReturnType.IsValueType ? Activator.CreateInstance(method.ReturnType) : null;
}
public class Facts : IGameFacts {
    public HashSet<string> Mods = [];
    public List<(string Domain, string Name, string Json)> Files = [];
    public IEnumerable<(string Domain, string Name, string Json)> Chapters() => Files;
    public IEnumerable<(string Domain, string Json)> Questlines() => [("questline", "{}")];
    public bool IsModLoaded(string id) => Mods.Contains(id);
    public bool CollectibleExists(string code) => true;
    public bool AnyMatches(string kind, string pattern) => true;
    public bool HasLang(string key) => true;
    public byte[] Texture(string location) => null;
}
