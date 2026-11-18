using System.Linq;
using System.Threading.Tasks;
using questline;
using questline.Client;
using questline.Model;
using questline.Server;
using Vintagestory.API.Common;
using Vintagestory.API.Config;
using Vintagestory.API.Util;
using Vintagestory.GameContent;
using VsTestkit.Testing;
using static VsTestkit.Testing.Vs;

namespace Questline.Tests
{
    /// <summary>
    /// The questline Questline ships: all of vanilla, stone age to steel and sailboats. It loads
    /// whole, every quest has its text, the recipe graph and the spoiler rule find nothing wrong
    /// with it, and it links every one of the game's own guides.
    /// </summary>
    [SingleplayerOnly]
    public class VanillaQuestlineTests
    {
        static QuestEngine Engine => Sapi.ModLoader.GetModSystem<QuestlineModSystem>().Engine;

        [VsTest(TimeoutMs = 60000)]
        public async Task TheDefaultQuestlineLoadsCleanly()
        {
            await OnServer();
            await Until(() => Engine.GraphChecksDone, 1200, "the graph checks, built in the background");
            var chapters = Engine.Registry.Chapters.Where(c => c.Id.StartsWith("questline:")).ToList();
            var problems = Engine.Problems.Where(p => p.StartsWith("questline:")).ToList();
            foreach (var p in problems) Log(p);
            Log($"{chapters.Count} chapters, {chapters.Sum(c => c.Quests.Count)} quests");

            Assert.Equal(0, problems.Count, "no problems in the default questline");
            Assert.Equal(25, chapters.Count(c => c.RequiresMod.Length == 0), "every part of vanilla, beside any chapters for installed mods");
            Assert.True(chapters.All(c => c.Questline == QuestRegistry.DefaultQuestline));
            Assert.True(chapters.All(c => c.Quests.Count >= 5), "no chapter left a stub");
            Assert.Greater(chapters.Sum(c => c.Quests.Count), 200);
        }

        /// <summary>The stone-tool quests: the quest, which of its tasks, and the head knapped for it.</summary>
        static readonly (string Quest, int Task, string Head)[] Heads =
        [
            ("knap-axe-head", 0, "axehead"), ("knap-knife", 0, "knifeblade"), ("knap-spear", 0, "spearhead"),
            ("knap-shovel", 0, "shovelhead"), ("knap-hoe", 0, "hoehead"), ("knap-arrowheads", 0, "arrowhead"),
        ];

        /// <summary>The quests for the tools made from those heads.</summary>
        static readonly (string Quest, int Task, string Head)[] Tools =
        [
            ("make-axe", 0, "axehead"), ("make-knife", 0, "knifeblade"), ("make-spear", 0, "spearhead"),
            ("knap-shovel", 1, "shovelhead"), ("make-hoe", 0, "hoehead"),
        ];

        /// <summary>
        /// A stone tool counts however it was made: every head the game knaps, and every tool a grid
        /// recipe makes from one, on a stick or a bone, in any stone. The heads and recipes come from
        /// the running game, so a pack's (String Sense's cords, another mod's stones) are held to it too.
        /// </summary>
        [VsTest]
        public async Task StoneToolsCountHoweverTheyAreMade()
        {
            await OnServer();
            var knapped = Sapi.GetKnappingRecipes().Select(r => r.Output.ResolvedItemstack?.Collectible?.Code).Where(c => c != null).ToHashSet();
            AssetLocation Pattern(string quest, int task)
            {
                var def = Engine.Registry.Get("questline:" + quest);
                Assert.NotNull(def, quest + " is in the default questline");
                return new AssetLocation(def.Tasks[task].Target);
            }
            foreach (var (quest, task, head) in Heads)
            {
                var pattern = Pattern(quest, task);
                var heads = knapped.Where(c => c.Path.StartsWith(head + "-")).ToList();
                Assert.True(heads.Count > 1, $"the game knaps {head} from more than one stone");
                foreach (var code in heads) Assert.True(WildcardUtil.Match(pattern, code), $"{quest} takes {code}");
            }
            foreach (var (quest, task, head) in Tools)
            {
                var pattern = Pattern(quest, task);
                var made = Sapi.World.GridRecipes
                    .Where(r => r.ResolvedIngredients?.Any(i => i?.ResolvedItemStack?.Collectible?.Code is { } c && knapped.Contains(c) && c.Path.StartsWith(head + "-")) == true)
                    .Select(r => r.Output.ResolvedItemStack?.Collectible?.Code).Where(c => c != null).Distinct().ToList();
                Assert.True(made.Count > 1, $"grid recipes make a tool from {head}");
                foreach (var code in made) Assert.True(WildcardUtil.Match(pattern, code), $"{quest} takes {code}");
            }
        }

        /// <summary>
        /// Every task in the default questline that takes many things names what they share ("any
        /// clay"), or says so itself ("any fruit"), rather than one of them ("any blue clay"), and
        /// none shows an untranslated name.
        /// </summary>
        [VsTest, RequiresClient]
        public async Task PatternTasksNameWhatTheyShare()
        {
            await OnClient();
            var client = Capi.ModLoader.GetModSystem<QuestlineModSystem>().Client;
            await Until(() => client.Ready, 200, "definitions on the client");
            var text = new QuestText(Capi, client);
            // A lang key as the game shows one it can't find, or a template it couldn't fill (mealrecipe-name--in-container).
            var untranslated = new System.Text.RegularExpressions.Regex(@"[a-z0-9_-]+:(block|item)-|\b[a-z0-9]+(-[a-z0-9]*){2,}\b");
            int faults = 0;
            foreach (var quest in client.Registry.Quests.Values.Where(q => q.Id.StartsWith("questline:")))
            {
                foreach (var task in quest.Tasks.Where(t => t.OnCollectible && TaskDef.IsPattern(t.Target)))
                {
                    string line = text.TaskLine(task);
                    Log($"{quest.Id}: {line}");
                    if (task.Name == null && text.SharedName(task.Target) == null) { Log($"  {task.Target} has no shared name"); faults++; }
                    if (untranslated.IsMatch(line)) { Log("  untranslated"); faults++; }
                }
            }
            Assert.Equal(0, faults, "every pattern task named");
            var findClay = client.Registry.Get("questline:find-clay").Tasks[0];
            Assert.Equal(Lang.Get("questline:task-obtain", Lang.Get("questline:any-of", "clay")), text.TaskLine(findClay), "clay, whatever its colour");
        }

        [VsTest(TimeoutMs = 60000)]
        public async Task EveryQuestCanBeReachedFromTheStart()
        {
            await OnServer();
            var quests = Engine.Registry.Quests.Values.Where(q => q.Id.StartsWith("questline:")).ToList();
            var reachable = new System.Collections.Generic.HashSet<string>();
            bool changed = true;
            while (changed)
            {
                changed = false;
                foreach (var q in quests.Where(q => !reachable.Contains(q.Id)))
                {
                    if (q.Requires == null || q.Requires.QuestIds().All(reachable.Contains))
                    {
                        reachable.Add(q.Id);
                        changed = true;
                    }
                }
            }
            foreach (var q in quests.Where(q => !reachable.Contains(q.Id))) Log("unreachable: " + q.Id);
            Assert.Equal(quests.Count, reachable.Count, "every quest reachable by doing the ones before it");
        }

        /// <summary>
        /// Questline's text is English only, and the game shows English where a language has no
        /// entry, so on a German game nothing is missing either.
        /// </summary>
        [VsTest(TimeoutMs = 60000)]
        public async Task TextCountsInAnotherLanguage()
        {
            await OnServer();
            string language = Lang.CurrentLocale;
            var english = Engine.Problems.Where(p => p.Contains("no lang entry")).ToHashSet();
            try
            {
                Lang.ChangeLanguage("de");
                Engine.Reload();
                var missing = Engine.Problems.Where(p => p.Contains("no lang entry") && !english.Contains(p)).ToList();
                foreach (var p in missing.Take(5)) Log(p);
                Assert.Equal(0, missing.Count, "English text counts when the game is in German");
            }
            finally
            {
                Lang.ChangeLanguage(language);
                Engine.Reload();
            }
        }

        /// <summary>Ordinary quests and milestones expose only one tiny cookie, not resource choices.</summary>
        [VsTest(TimeoutMs = 30000)]
        public async Task QuestAndMilestoneRewardsAreOnlyCookies()
        {
            await OnServer();
            var rewarded = Engine.Registry.Quests.Values
                .Where(q => q.Id.StartsWith("questline:") && q.Rewards.Count > 0).ToList();
            Assert.True(rewarded.Count > 0, "content addon supplies rewarded quests");
            Assert.True(rewarded.Any(q => q.Shape == NodeShape.Gear), "milestones included");
            foreach (var quest in rewarded)
            {
                Assert.Equal(1, quest.Rewards.Count, quest.Id);
                var reward = quest.Rewards.Single();
                Assert.Equal("item", reward.Type, quest.Id);
                Assert.Equal(RewardPolicy.CookieCode, reward.Item, quest.Id);
                Assert.Equal(1, reward.Count, quest.Id);
            }
            string before = Engine.Registry.ToJson();
            foreach (double multiplier in new[] { 0d, 0.5, 100 })
                Assert.Equal(before, Engine.Registry.WithRewards(new QuestlineConfig { GearRewards = multiplier }).ToJson(), "legacy multiplier cannot restore resources or change cookie quantity");
        }

        /// <summary>
        /// The ages run stone, clay and fire, copper, bronze, iron and steel, and a quest in a themed
        /// chapter belongs to the age the game actually gates it behind.
        /// </summary>
        [VsTest(TimeoutMs = 30000)]
        public async Task QuestsBelongToTheAgeTheyNeed()
        {
            await OnServer();
            var registry = Engine.Registry;
            var ages = registry.Chapters.Where(c => c.Age && c.Id.StartsWith("questline:")).Select(c => c.Id[10..]);
            Assert.Equal("stone-age, clay-and-fire, copper-age, bronze-age, iron-age, steel-age", string.Join(", ", ages));
            string AgeOf(string id) => registry.AgeOf(registry.Get("questline:" + id))?.Id[10..];
            Assert.Equal("stone-age", AgeOf("knap-hoe"));
            // The quern takes a metal hammer and chisel; the pie's table, a saw.
            Assert.Equal("copper-age", AgeOf("make-quern"));
            Assert.Equal("copper-age", AgeOf("bake-pie"));
            Assert.Equal("iron-age", AgeOf("build-greenhouse"));
            Assert.Equal("steel-age", AgeOf("make-steel-plate"));
        }

        /// <summary>
        /// Each chapter reads left to right: a prerequisite in the same chapter sits to the left of
        /// what it unlocks, no two quests crowd one another, and no line passes behind a quest.
        /// </summary>
        [VsTest(TimeoutMs = 60000)]
        public async Task EveryChapterReadsLeftToRight()
        {
            await OnServer();
            int faults = 0;
            void Fault(string why) { Log(why); faults++; }
            foreach (var chapter in Engine.Registry.Chapters.Where(c => c.Id.StartsWith("questline:")))
            {
                var quests = chapter.Quests;
                var byId = quests.ToDictionary(q => q.Id);
                for (int i = 0; i < quests.Count; i++)
                {
                    for (int j = i + 1; j < quests.Count; j++)
                    {
                        if (System.Math.Abs(quests[i].Pos[0] - quests[j].Pos[0]) < 2 && System.Math.Abs(quests[i].Pos[1] - quests[j].Pos[1]) < 1.5f) Fault($"{quests[i].Id} and {quests[j].Id} crowd each other");
                    }
                }
                foreach (var quest in quests)
                {
                    foreach (string id in quest.Requires?.QuestIds() ?? [])
                    {
                        if (!byId.TryGetValue(id, out var before)) continue;
                        float px = before.Pos[0], py = before.Pos[1], vx = quest.Pos[0] - px, vy = quest.Pos[1] - py;
                        if (vx <= 0) Fault($"{id} isn't left of {quest.Id}");
                        foreach (var other in quests.Where(o => o != quest && o != before))
                        {
                            float u = ((other.Pos[0] - px) * vx + (other.Pos[1] - py) * vy) / (vx * vx + vy * vy);
                            if (u <= 0 || u >= 1) continue;
                            float dx = px + u * vx - other.Pos[0], dy = py + u * vy - other.Pos[1];
                            if (dx * dx + dy * dy < 0.45f * 0.45f) Fault($"the line {id} → {quest.Id} passes behind {other.Id}");
                        }
                    }
                }
            }
            Assert.Equal(0, faults, "every chapter laid out clearly");
        }

        /// <summary>The game's guides, as the handbook lists them: each one is linked from some quest's text.</summary>
        [VsTest(TimeoutMs = 60000), RequiresClient]
        public async Task EveryVanillaGuideIsLinked()
        {
            await OnServer();
            var quests = Engine.Registry.Quests.Values.Where(q => q.Id.StartsWith("questline:")).ToList();
            await OnClient();
            // The game's own guides only: mods' guides (Expanded Foods ships several) are theirs to teach.
            string vanilla = System.IO.Path.GetFullPath(Vintagestory.API.Config.GamePaths.AssetsPath);
            var guides = Capi.Assets.GetMany("config/handbook")
                .Where(a => a.Origin?.OriginPath != null && System.IO.Path.GetFullPath(a.Origin.OriginPath).StartsWith(vanilla))
                .Select(a => a.ToObject<Vintagestory.GameContent.GuiHandbookTextPage>()?.PageCode)
                .Where(code => code != null)
                .ToList();
            Assert.Greater(guides.Count, 25, "the game's guides found");

            var text = string.Join("\n", quests.Select(q => Vintagestory.API.Config.Lang.Get(q.Id + "-desc")));
            var missing = guides.Where(code => !text.Contains("handbook://" + code + "\"")).ToList();
            foreach (string code in missing) Log("not linked: " + code);
            Assert.Equal(0, missing.Count, "every guide linked from a quest");
        }

        /// <summary>Photographs every chapter as a new player first sees it, at the test window's 960×600, for review.</summary>
        [VsTest(TimeoutMs = 300000), RequiresClient]
        public async Task EveryChapterPhotographed()
        {
            await OnServer();
            var ids = Engine.Registry.Chapters.Where(c => c.Id.StartsWith("questline:")).OrderBy(c => c.Order).Select(c => c.Id).ToList();
            await OnClient();
            var book = Capi.ModLoader.GetModSystem<QuestlineModSystem>().Book;
            foreach (string id in ids)
            {
                book.ForgetViews();
                book.SelectChapter(id);
                await VsTestkit.Testing.Gui.WaitFor<questline.Client.GuiDialogQuestBook>();
                await Frames.Wait(20);
                Log(await Shot.Take($"questline-chapter-{id[10..]}.png"));
            }
            // A milestone's page, with its choice of three rewards.
            book.SelectQuest("questline:first-smithing");
            await Frames.Wait(20);
            Log(await Shot.Take("questline-chapter-milestone-reward.png"));
            book.TryClose();
        }

        /// <summary>Every quest that isn't ticked by hand gives something, and every milestone offers a choice.</summary>
        [VsTest(TimeoutMs = 30000)]
        public async Task QuestsGiveRewardsAndMilestonesAChoice()
        {
            await OnServer();
            var quests = Engine.Registry.Quests.Values.Where(q => q.Id.StartsWith("questline:")).ToList();
            var bare = quests.Where(q => q.Rewards.Count == 0 && q.Tasks.Any(t => t.Type != "checkbox")).ToList();
            foreach (var q in bare) Log("no reward: " + q.Id);
            Assert.Equal(0, bare.Count, "every quest with real tasks rewards the player");

            var milestones = quests.Where(q => q.Shape == NodeShape.Gear).ToList();
            foreach (var q in milestones.Where(q => !q.Rewards.Any(r => r.Type == "choice"))) Log("milestone without a choice: " + q.Id);
            Assert.True(milestones.All(q => q.Rewards.Any(r => r.Type == "choice" && r.Options.Count == 3)), "each milestone offers three");
        }
    }
}
