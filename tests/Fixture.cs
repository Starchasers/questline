using Vintagestory.API.Common;
using VsTestkit.Testing;
using static VsTestkit.Testing.Vs;

namespace Questline.Tests
{
    /// <summary>The qltest fixture mod (tests/fixtures/Mods), whose chapters most suites test against.</summary>
    static class Fixture
    {
        /// <summary>
        /// Skips the test when the fixture mod isn't loaded, and fails it when the mod is loaded but
        /// its quests aren't. Asking only whether a fixture quest exists also skips when Questline
        /// itself failed to start, and that is how a crash at startup once passed for a missing fixture.
        /// </summary>
        public static void Require(ICoreAPI api, bool questsLoaded)
        {
            if (!api.ModLoader.IsModEnabled("qltest")) Skip("the qltest fixture isn't loaded; pass --mods tests/fixtures/Mods");
            Assert.True(questsLoaded, "the qltest fixture is loaded, so its quests should be; did Questline start?");
        }
    }
}
