using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using questline;
using questline.Model;

// Dependency-free, headless executable regression tests. These exercise real framework
// code and asset contracts, not a running game or the unavailable VsTestkit.
const string Cookie = "questline:questcookie";
string root = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "../../../../../"));
int passed = 0, failed = 0;
void Check(bool ok, string message) { if (!ok) throw new Exception(message); }
void Test(string name, Action run)
{
    try { run(); passed++; Console.WriteLine("PASS " + name); }
    catch (Exception e) { failed++; Console.WriteLine("FAIL " + name + ": " + e); }
}
RewardDef Item(string code, int count = 1) => new() { Type = "item", Item = code, Count = count };
QuestRegistry Registry(params RewardDef[] rewards)
{
    var r = new QuestRegistry { Chapters = [new() { Id = "test:chapter", Quests = [new() {
        Id = "test:quest", Shape = NodeShape.Gear, Rewards = rewards.ToList(),
        Tasks = [new() { Type = "obtain", Item = "game:stone-granite", Count = 3, Consume = true }],
        Page = [new() { Type = "text", Lang = "test:prose" }]
    }] }] };
    r.Index(); return r;
}
QuestDef Effective(QuestRegistry r, QuestlineConfig config = null) => r.WithRewards(config ?? new()).Get("test:quest");
void OnlyCookie(QuestDef q)
{
    Check(q.Rewards.Count == 1, $"expected one reward, got {q.Rewards.Count}");
    Check(q.Rewards[0].Type == "item" && q.Rewards[0].Item == Cookie && q.Rewards[0].Count == 1,
        "original payout survived instead of one Quest Cookie: " + JsonConvert.SerializeObject(q.Rewards));
}
Test("ordinary resource payout becomes one cookie", () => OnlyCookie(Effective(Registry(Item("game:gear-rusty", 100)))));
Test("milestone bundles and resource choices become one cookie", () => OnlyCookie(Effective(Registry(
    Item("game:ingot-iron", 8), Item("game:gear-rusty", 40), new() { Type = "choice", Options = [Item("game:diamond", 5), Item("game:flaxfibers", 32)] }))));
Test("gear multiplier cannot scale or suppress cookie", () => {
    foreach (double multiplier in new[] { 0d, 0.5, 100 }) OnlyCookie(Effective(Registry(Item("game:gear-rusty", 7)), new() { GearRewards = multiplier }));
});
Test("source registry and non-reward fields are preserved", () => {
    var source = Registry(Item("game:ingot-iron", 8)); string before = source.ToJson();
    var effective = Effective(source);
    Check(source.ToJson() == before, "projection mutated source metadata");
    var a = JObject.Parse(JsonConvert.SerializeObject(source.Get("test:quest")));
    var b = JObject.Parse(JsonConvert.SerializeObject(effective)); a.Remove("Rewards"); b.Remove("Rewards");
    Check(JToken.DeepEquals(a, b), "non-reward quest fields changed");
});
Test("network roundtrip and repeated projection are idempotent", () => {
    var r = Registry(Item("game:gear-rusty", 9)).WithRewards(new());
    var client = QuestRegistry.FromJson(r.ToJson()); OnlyCookie(client.Get("test:quest"));
    Check(client.ToJson() == client.WithRewards(new()).ToJson(), "projection not idempotent");
});
Test("stage grants and explicit item-rewards opt-out remain", () => {
    var r = Registry(Item("game:gear-rusty", 4), new() { Type = "stage", Stage = "test:copper" });
    var on = Effective(r); Check(on.Rewards.Count == 2 && on.Rewards.Any(x => x.Type == "stage" && x.Stage == "test:copper"), "lost stage");
    var off = Effective(r, new() { ItemRewards = false });
    Check(off.Rewards.Count == 1 && off.Rewards[0].Stage == "test:copper", "opt-out lost stage or gave items");
    Check(Effective(Registry()).Rewards.Count == 0, "invented reward on rewardless quest");
});
Test("completed claimed progress and consumption survive projection", () => {
    var q = Effective(Registry(Item("game:gear-rusty", 4)));
    var p = new PlayerProgress(); var qp = p.GetOrCreate(q); qp.Tasks[0] = 3; qp.Complete = true; qp.Consumed = true; qp.Claimed = true;
    var restored = JsonConvert.DeserializeObject<PlayerProgress>(JsonConvert.SerializeObject(p));
    Check(PlayerProgress.StateOf(q, restored.Find(q.Id), true, true) == QuestState.Done, "claimed quest reopened");
    Check(restored.Find(q.Id).Consumed && restored.Find(q.Id).Tasks[0] == 3, "consumption/progress lost");
    Check(PlayerProgress.StateOf(q, qp, false, true) == QuestState.Claimable, "cookie not claimable");
});
Test("all shipping item payouts including milestones project to cookie", () => {
    string content = Path.Combine(root, "content");
    var paths = Directory.Exists(content) ? Directory.GetFiles(content, "*.json", SearchOption.AllDirectories).Where(p => p.Contains("/chapters/"))
        : Directory.GetFiles(Path.Combine(root, "questline/assets"), "*.json", SearchOption.AllDirectories).Where(p => p.Contains("/chapters/"));
    int quests = 0, milestones = 0;
    foreach (string file in paths) {
        var chapter = JsonConvert.DeserializeObject<ChapterDef>(File.ReadAllText(file));
        foreach (var q in chapter.Quests.Where(q => q.Rewards.Count > 0)) {
            var r = new QuestRegistry { Chapters = [new() { Id = "shipping", Quests = [q] }] }; r.Index();
            OnlyCookie(r.WithRewards(new()).Get(q.Id)); quests++; if (q.Shape == NodeShape.Gear) milestones++;
        }
    }
    Check(quests > 400 && milestones > 0, $"shipping corpus unexpectedly narrow: {quests} rewarded quests, {milestones} milestones");
    Console.WriteLine($"  exercised {quests} rewarded quests including {milestones} milestones");
});
Test("cookie asset is isolated nonspoiling tiny food with no transformations", () => {
    var path = Path.Combine(root, "questline/assets/questline/itemtypes/questcookie.json");
    Check(File.Exists(path), "missing cookie item asset"); var item = JObject.Parse(File.ReadAllText(path));
    Check((string)item["code"] == "questcookie" && (string)item["class"] == "Item", "cookie must be plain isolated Item");
    var n = (JObject)item["nutritionProps"];
    Check(n != null && (double)n["satiety"] == 10 && ((double?)n["health"] ?? 0) == 0, "expected satiety 10, no healing");
    string[] allowed = ["code", "class", "maxstacksize", "texture", "shape", "nutritionProps", "creativeinventory", "heldTpIdleAnimation", "heldTpUseAnimation", "guiTransform", "fpHandTransform", "tpHandTransform", "groundTransform"];
    Check(item.Properties().All(p => allowed.Contains(p.Name)), "unexpected behavior, attributes, fuel/feed or processing property");
    Check(n.Properties().All(p => p.Name is "satiety" or "foodcategory" or "health"), "unexpected nutrition effect");
    var lang = JObject.Parse(File.ReadAllText(Path.Combine(root, "questline/assets/questline/lang/en.json")));
    Check((string)lang["item-questcookie"] == "Quest Cookie", "missing English name");
    string texture = (string)item["texture"]["base"];
    Check(texture == "questline:item/questcookie", "must use owned isolated texture");
    Check(File.Exists(Path.Combine(root, "questline/assets/questline/textures/item/questcookie.png")), "missing owned texture");
    Check(!Directory.GetFiles(Path.Combine(root, "questline/assets"), "*.json", SearchOption.AllDirectories)
        .Where(p => p.Contains("/recipes/")).Any(p => File.ReadAllText(p).Contains("questcookie")), "cookie recipe supplied");
});
Test("real Claim rejects incomplete/repeated claims and only mints cookie", () => {
    var r = Registry(Item("game:ingot-iron", 64), Item("game:gear-rusty", 12));
    var q = r.Get("test:quest"); q.Tasks[0].Consume = false;
    var f = new ClaimFixture(r);
    Check(f.Engine.Claim(f.A, q.Id, null) != null && f.Given.Count == 0, "incomplete quest paid out");
    f.Complete(q, "a"); Check(f.Engine.Claim(f.A, q.Id, null) == null, "first claim refused");
    Check(f.Given.Count == 1 && f.Given[0] == (Cookie, 1), "not exactly one cookie");
    Check(f.Lookups.SequenceEqual(new[] { Cookie }), "looked up original resource");
    Check(f.Engine.ProgressOf("a").Find(q.Id).Consumed, "consumption guard not persisted");
    Check(f.Engine.Claim(f.A, q.Id, null) != null && f.Given.Count == 1, "duplicate payout");
});
Test("real Claim cannot consume/mark claimed when hand-in items are absent", () => {
    var r = Registry(Item("game:gear-rusty", 4)); var q = r.Get("test:quest"); var f = new ClaimFixture(r); f.Complete(q, "a");
    Check(f.Engine.Claim(f.A, q.Id, null) != null, "missing hand-in accepted");
    var p = f.Engine.ProgressOf("a").Find(q.Id);
    Check(!p.Consumed && !p.Claimed && p.Complete && p.Tasks[0] == 3 && f.Given.Count == 0, "failed hand-in mutated progress or paid out");
});
Test("real milestone server-first and per-player claims retain scope", () => {
    foreach (var mode in new[] { ClaimMode.First, ClaimMode.Each }) {
        var r = Registry(Item("game:ingot-iron", 32)); var q = r.Get("test:quest"); q.Tasks.Clear(); q.Mode = QuestMode.Server; q.Claim = mode;
        var f = new ClaimFixture(r); f.Complete(q, "a");
        Check(f.Engine.Claim(f.A, q.Id, null) == null, "first server claim refused");
        string second = f.Engine.Claim(f.B, q.Id, null);
        Check((second == null) == (mode == ClaimMode.Each), "server claim scope changed");
        Check(f.Given.Count == (mode == ClaimMode.First ? 1 : 2) && f.Given.All(x => x == (Cookie, 1)), "wrong scoped payout");
    }
});
Test("real party claims remain once per member with shared completion", () => {
    var r = Registry(Item("game:ingot-iron", 32)); var q = r.Get("test:quest"); q.Tasks.Clear(); q.Mode = QuestMode.Party;
    var f = new ClaimFixture(r); var (party, error) = f.Engine.CreateParty("a", "Cookie testers");
    Check(error == null && f.Engine.Invite("a", "b") == null && f.Engine.Accept("b", party.Id) == null, "party setup failed");
    f.Complete(q, "a");
    Check(f.Engine.Claim(f.A, q.Id, null) == null, "first member refused");
    Check(f.Engine.StateOf("b", q.Id) == QuestState.Claimable, "first member took second member's claim");
    Check(f.Engine.Claim(f.B, q.Id, null) == null && f.Engine.Claim(f.A, q.Id, null) != null, "party claim ownership changed");
    Check(f.Given.Count == 2 && f.Given.All(x => x == (Cookie, 1)), "party received original materials or duplicate cookies");
});
Test("real Claim still grants stages with item opt-out", () => {
    var r = Registry(Item("game:gear-rusty", 4), new() { Type = "stage", Stage = "test:stage" });
    var q = r.Get("test:quest"); q.Tasks.Clear(); var f = new ClaimFixture(r); f.Engine.Config.ItemRewards = false; f.Complete(q, "a");
    Check(f.Engine.Claim(f.A, q.Id, null) == null && f.Engine.HasStage("a", "test:stage"), "stage reward lost");
    Check(f.Given.Count == 0 && f.Engine.ProgressOf("a").Find(q.Id).Claimed, "opt-out paid items or lost claim");
});
Test("stage-bearing choices stay choices and cookie asset nutrition parses in game API", () => {
    var r = Registry(new RewardDef { Type = "choice", Options = [Item("game:diamond", 9), new() { Type = "stage", Stage = "test:choice" }] });
    var q = Effective(r); q.Tasks.Clear();
    Check(q.Rewards.Count == 1 && q.Rewards[0].Type == "choice" && q.Rewards[0].Options.Count == 2, "stage-bearing choice collapsed");
    var f = new ClaimFixture(new QuestRegistry { Chapters = [new() { Id = "mixed", Quests = [q] }] }); f.Engine.Registry.Index(); f.Complete(q, "a");
    Check(f.Engine.Claim(f.A, q.Id, null) != null && f.Given.Count == 0, "unpicked mixed choice paid out");
    Check(f.Engine.Claim(f.A, q.Id, [1]) == null && f.Engine.HasStage("a", "test:choice"), "chosen stage lost");
    var item = JObject.Parse(File.ReadAllText(Path.Combine(root, "questline/assets/questline/itemtypes/questcookie.json")));
    var props = item["nutritionProps"].ToObject<Vintagestory.API.Common.FoodNutritionProperties>();
    Check(props.Satiety == 10 && props.Health == 0 && props.FoodCategory == Vintagestory.API.Common.EnumFoodCategory.NoNutrition, "nutrition rejected or imparts nutrition buffs");
});
Test("real Claim rejects unknown rewards recursively before any mutation in both opt-out modes", () => {
    foreach (bool items in new[] { true, false })
    foreach (string type in new string[] { "custom", "unknown", null, "ITEM" })
    foreach (bool choice in new[] { false, true }) {
        var bad = new RewardDef { Type = type, Item = "game:diamond", Count = 50 };
        var r = Registry(choice ? new() { Type = "choice", Options = [bad, new() { Type = "stage", Stage = "test:stage" }] } : bad);
        var q = r.Get("test:quest"); var f = new ClaimFixture(r); f.Engine.Config.ItemRewards = items;
        f.Carry("a", "game:stone-granite", 3); f.Complete(q, "a");
        Check(f.Engine.Claim(f.A, q.Id, [0]) != null, "unknown reward accepted");
        var p = f.Engine.ProgressOf("a").Find(q.Id);
        Check(!p.Claimed && !p.Consumed && f.CarriedA[0].StackSize == 3 && f.Lookups.Count == 0 && f.Given.Count == 0, "invalid reward mutated or dispatched");
    }
});
Test("real Claim rejects nested choices and invalid stages without exception or hand-in loss", () => {
    foreach (var bad in new RewardDef[] {
        new() { Type = "choice", Options = [new() { Type = "choice", Options = [Item("game:diamond", 50), new() { Type = "stage", Stage = "test:stage" }] }, new() { Type = "stage", Stage = "test:outer" }] },
        new() { Type = "choice", Options = [Item("game:diamond"), new() { Type = "stage", Stage = " " }] },
        new() { Type = "choice", Options = [] }
    }) {
        var r = Registry(bad); var q = r.Get("test:quest"); var f = new ClaimFixture(r);
        f.Carry("a", "game:stone-granite", 3); f.Complete(q, "a");
        Check(f.Engine.Claim(f.A, q.Id, [0]) != null, "invalid tree accepted");
        var p = f.Engine.ProgressOf("a").Find(q.Id);
        Check(!p.Claimed && !p.Consumed && f.CarriedA[0].StackSize == 3 && f.Given.Count == 0, "invalid tree mutated claim");
    }
});
Test("real Claim preflights missing cookie before hand-in or stage mutation and permits retry", () => {
    var r = Registry(new() { Type = "stage", Stage = "test:stage" }, Item("game:diamond", 50));
    var q = r.Get("test:quest"); var f = new ClaimFixture(r) { MissingCookie = true };
    f.Carry("a", "game:stone-granite", 3); f.Complete(q, "a");
    Check(f.Engine.Claim(f.A, q.Id, null) != null, "missing cookie accepted");
    var p = f.Engine.ProgressOf("a").Find(q.Id);
    Check(!p.Claimed && !p.Consumed && !f.Engine.HasStage("a", "test:stage") && f.CarriedA[0].StackSize == 3 && f.Given.Count == 0, "missing cookie burned progress/hand-in");
    Check(f.Lookups.All(x => x == Cookie), "legacy fallback lookup");
    f.MissingCookie = false;
    Check(f.Engine.Claim(f.A, q.Id, null) == null && f.Given.SequenceEqual(new[] { (Cookie, 1) }), "retry after asset restored failed");
});
Test("real Claim successful hand-in consumes exactly once in personal party and server scopes", () => {
    foreach (var mode in new[] { QuestMode.Individual, QuestMode.Party, QuestMode.Server }) {
        var r = Registry(Item("game:diamond", 50)); var q = r.Get("test:quest"); q.Mode = mode;
        var f = new ClaimFixture(r);
        if (mode == QuestMode.Party) { var (party, error) = f.Engine.CreateParty("a", "shared"); Check(error == null && f.Engine.Invite("a", "b") == null && f.Engine.Accept("b", party.Id) == null, "party setup"); }
        f.Carry("a", "game:stone-granite", mode == QuestMode.Individual ? 6 : 1);
        f.Carry("b", "game:stone-granite", 5); f.Complete(q, "a");
        Check(f.Engine.Claim(f.A, q.Id, null) == null, "hand-in failed");
        Check(f.CarriedA[0].StackSize == (mode == QuestMode.Individual ? 3 : 0) && f.CarriedB[0].StackSize == (mode == QuestMode.Individual ? 5 : 3), "wrong hand-in amount/order");
        Check(f.Engine.Claim(f.A, q.Id, null) != null, "duplicate claim");
        if (mode != QuestMode.Individual) Check(f.Engine.Claim(f.B, q.Id, null) == null && f.CarriedB[0].StackSize == 3 && f.Given.Count == 2, "shared hand-in consumed twice");
    }
});
Test("real Claim drops exactly one cookie on inventory overflow", () => {
    var r = Registry(Item("game:diamond", 50)); var q = r.Get("test:quest"); q.Tasks[0].Consume = false;
    var f = new ClaimFixture(r) { InventoryFull = true }; f.Complete(q, "a");
    Check(f.Engine.Claim(f.A, q.Id, null) == null && f.Given.Count == 0 && f.Dropped.SequenceEqual(new[] { (Cookie, 1) }), "overflow not delivered as one cookie");
    Check(f.Engine.Claim(f.A, q.Id, null) != null && f.Dropped.Count == 1, "overflow duplicated");
});
Test("legacy save bytes load normalize claim save and load again without payout replay", () => {
    var r = Registry(Item("game:diamond", 50));
    var second = new QuestDef { Id = "test:claimed", Tasks = [new() { Type = "obtain", Item = "game:stone-granite", Count = 3, Consume = true }], Rewards = [Item("game:gear-rusty", 8)] };
    r.Chapters[0].Quests.Add(second); r.Index();
    var f = new ClaimFixture(r.WithRewards(new QuestlineConfig()));
    // Literal old-schema progress: the completed, unclaimed quest predates cookie policy.
    f.SaveData["questline-progress"] = System.Text.Encoding.UTF8.GetBytes("""
    {"a":{"Quests":{"test:quest":{"Tasks":[3],"Complete":true,"Claimed":false,"Consumed":false,"Seeded":true,"CompletedDay":12.5},"test:claimed":{"Tasks":[3],"Complete":true,"Claimed":true,"Consumed":true}},"Stages":["legacy:stage"],"History":{"craft|game:stone":9}}}
    """);
    f.Engine.LoadProgress(); var q = f.Engine.Registry.Get("test:quest");
    Check(f.Engine.ProgressOf("a").Find(q.Id).CompletedDay == 12.5 && f.Engine.HasStage("a", "legacy:stage"), "legacy state lost");
    f.Carry("a", "game:stone-granite", 6);
    Check(f.Engine.Claim(f.A, "test:claimed", null) != null && f.Given.Count == 0, "claimed legacy quest replayed");
    Check(f.Engine.Claim(f.A, q.Id, null) == null && f.Given.SequenceEqual(new[] { (Cookie, 1) }) && f.CarriedA[0].StackSize == 3, "pending legacy claim wrong payout/hand-in");
    f.Engine.SaveProgress(); typeof(questline.Server.QuestEngine).GetProperty("Registry").SetValue(f.Engine, r.WithRewards(new QuestlineConfig())); f.Engine.LoadProgress();
    Check(f.Engine.Claim(f.A, q.Id, null) != null && f.Given.Count == 1 && f.CarriedA[0].StackSize == 3, "reload replayed claim/consumption");
    var p = f.Engine.ProgressOf("a");
    Check(p.Find(q.Id).Claimed && p.Find(q.Id).Consumed && p.History["craft|game:stone"] == 9 && p.Stages.Contains("legacy:stage"), "roundtrip state lost");
});
Console.WriteLine($"RESULT {passed} passed, {failed} failed");
return failed == 0 ? 0 : 1;
