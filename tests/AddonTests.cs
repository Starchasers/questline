using System.Linq;
using System.Threading.Tasks;
using questline;
using questline.Server;
using VsTestkit.Testing;
using static VsTestkit.Testing.Vs;

namespace Questline.Tests
{
    /// <summary>
    /// Chapters that extend another chapter, as the mod addons do: their quests join it when their
    /// mods are installed, and stay out, quietly, when they aren't.
    /// </summary>
    [SingleplayerOnly]
    public class AddonTests
    {
        static QuestEngine Engine => Sapi.ModLoader.GetModSystem<QuestlineModSystem>().Engine;

        [VsTest]
        public async Task AnExtensionJoinsItsChapterOnlyWithItsMods()
        {
            await OnServer();
            Fixture.Require(Sapi, Engine.Registry.ChaptersById.TryGetValue("qltest:workshop", out var workshop));

            var ids = workshop.Quests.Select(q => q.Id).ToList();
            Log(string.Join(", ", ids));
            Assert.True(ids.Contains("qltest:workshop-addon"), "the extension for a loaded mod joined");
            Assert.False(ids.Contains("qltest:workshop-absent"), "the extension for a missing mod stayed out");
            Assert.Equal("qltest:workshop", Engine.Registry.Get("qltest:workshop-addon").ChapterId);
            Assert.Equal(1, workshop.Art.Count, "its art came too");
            Assert.Equal("obtain", Engine.Registry.Get("qltest:workshop-start").Tasks[0].Type, "a quest of the same id replaced the chapter's own");
            Assert.Equal(2, workshop.Quests.Count, "replaced, not added");

            Assert.False(Engine.Registry.ChaptersById.ContainsKey("qltest:workshop-with-game"), "an extension isn't a chapter of its own");
            foreach (var p in Engine.Problems.Where(p => p.Contains("workshop"))) Log(p);
            Assert.False(Engine.Problems.Any(p => p.Contains("workshop")), "no problems from either");
        }

        /// <summary>
        /// Every structure worldgen recorded in loaded map regions is mapped by its config code.
        /// Keep generic visit-task support independent of any shipped content integration.
        /// </summary>
        [VsTest]
        public async Task GeneratedStructuresAreKnown()
        {
            await OnServer();
            var codes = Engine.Structures;

            int size = Sapi.WorldManager.RegionSize, found = 0;
            var unknown = new System.Collections.Generic.List<string>();
            var spawn = Sapi.World.DefaultSpawnPosition.AsBlockPos;
            for (int rx = spawn.X / size - 4; rx <= spawn.X / size + 4; rx++)
            {
                for (int rz = spawn.Z / size - 4; rz <= spawn.Z / size + 4; rz++)
                {
                    foreach (var placed in Sapi.WorldManager.GetMapRegion(rx, rz)?.GeneratedStructures?.ToList() ?? [])
                    {
                        found++;
                        if (codes.Of(placed).Count == 0) unknown.Add($"{placed.Code} ({placed.Group})");
                    }
                }
            }
            Log($"{found} structures recorded around spawn");
            foreach (string u in unknown.Distinct().Take(20)) Log("unknown: " + u);
            Assert.Equal(0, unknown.Count, "every recorded structure known by its config's code");
        }
    }
}
