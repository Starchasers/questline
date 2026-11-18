using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using HarmonyLib;
using questline;
using questline.Server;
using Questline.ToolsmithCompat;
using Vintagestory.API.Common;
using Vintagestory.API.Server;

// Real core/adapter assemblies and real Harmony, with synthetic provider targets only.
static class Program
{
    static readonly List<(IServerPlayer Player, string Type, string Code, int Amount)> Reports = new();
    static int checks;
    static EntityPlayer syntheticEntity;
    static IPlayer syntheticPlayer;
    // This substitutes player lookup, not native assembly/world semantics.
    static bool SyntheticPlayer(EntityPlayer __instance, ref IPlayer __result)
    {
        if (!ReferenceEquals(__instance, syntheticEntity)) return true;
        __result = syntheticPlayer;
        return false;
    }
    static bool Intercept(IServerPlayer player, string type, AssetLocation code, int amount)
    { Reports.Add((player, type, code.ToString(), amount)); return false; }
    static void Check(bool ok, string name)
    { if (!ok) throw new Exception(name); checks++; Console.WriteLine("PASS " + name); }
    public static ItemStack Output() => new(new Item { Code = new AssetLocation("game:axe-felling-copper") }, 2);
    static void Main()
    {
        var h = new Harmony("questline.toolsmith.tests");
        h.Patch(AccessTools.Method(typeof(QuestEngine), "Report", new[] { typeof(IServerPlayer), typeof(string), typeof(AssetLocation), typeof(int) }), prefix: new HarmonyMethod(typeof(Program), nameof(Intercept)));
        var api = new QuestlineApi();
        Assembly.Load("VintagestoryLib");
        var player = (IServerPlayer)RuntimeHelpers.GetUninitializedObject(AccessTools.TypeByName("Vintagestory.Server.ServerPlayer"));
        Check(!api.ReportCraft(player, new AssetLocation("game:axe")), "reject before initialization");
        AccessTools.Field(typeof(QuestlineApi), "engine").SetValue(api, RuntimeHelpers.GetUninitializedObject(typeof(QuestEngine)));
        Check(!api.ReportCraft(null, new AssetLocation("game:axe")), "reject null player");
        Check(!api.ReportCraft(player, null), "reject null code");
        Check(!api.ReportCraft(player, new AssetLocation("game:*")), "reject wildcard");
        Check(!api.ReportCraft(player, new AssetLocation("game:axe"), 0), "reject zero");
        Check(!api.ReportCraft(player, new AssetLocation("game:axe"), -1), "reject negative");
        Check(Reports.Count == 0, "invalid reports do not reach engine");
        api.Report(player, "test:custom", 3);
        Check(Reports[^1].Type == "custom" && Reports[^1].Amount == 3, "Report retains custom semantics");
        Check(api.ReportCraft(player, new AssetLocation("game:axe"), 4) && Reports[^1].Type == "craft" && Reports[^1].Amount == 4, "craft API forwards code/type/count");
        Reports.Clear();
        AccessTools.Field(typeof(ToolsmithCompatSystem), "progress").SetValue(null, api);
        var adapter = new Harmony(ToolsmithCompatSystem.HarmonyId);
        foreach (string name in new[] { "InHand", "WorkbenchStrike", "WorkbenchTool" })
            adapter.CreateClassProcessor(typeof(ToolsmithCompatSystem).GetNestedType(name, BindingFlags.NonPublic)).Patch();
        var bench = new Toolsmith.ToolTinkering.Blocks.BlockEntityWorkbench();
        bench.AttemptToCraft(player);
        Check(Reports.Count == 1 && Reports[0] == (player, "craft", "game:axe-felling-copper", 2), "workbench output credits striking player once");
        Toolsmith.ToolTinkering.TinkeringUtility.TryCraftToolFromSlots();
        Check(Reports.Count == 1, "unattributed output gives no credit");
        try { bench.AttemptToCraft(player, true); } catch (InvalidOperationException) { }
        Toolsmith.ToolTinkering.TinkeringUtility.TryCraftToolFromSlots();
        Check(Reports.Count == 1, "exception clears attribution");
        Toolsmith.ToolTinkering.TinkeringUtility.Empty = true;
        bench.AttemptToCraft(player);
        Check(Reports.Count == 1, "null workbench result gives no credit");
        Toolsmith.ToolTinkering.TinkeringUtility.Empty = false;
        var slot = new DummySlot(Output());
        Toolsmith.ToolTinkering.TinkeringUtility.AssembleFullTool(slot, null);
        Check(Reports.Count == 1, "unchanged in-hand bundle gives no credit");
        syntheticEntity = (EntityPlayer)RuntimeHelpers.GetUninitializedObject(typeof(EntityPlayer));
        syntheticPlayer = player;
        h.Patch(AccessTools.PropertyGetter(typeof(EntityPlayer), "Player"), prefix: new HarmonyMethod(typeof(Program), nameof(SyntheticPlayer)));
        Toolsmith.ToolTinkering.TinkeringUtility.ReplaceBundle = true;
        Toolsmith.ToolTinkering.TinkeringUtility.AssembleFullTool(slot, syntheticEntity);
        Check(Reports.Count == 2 && Reports[^1] == (player, "craft", "game:axe-felling-copper", 2), "synthetic in-hand replacement credits player/code/count once");
        Toolsmith.ToolTinkering.TinkeringUtility.AssembleFullTool(new DummySlot(Output()), null);
        Check(Reports.Count == 2, "in-hand replacement without player gives no credit");
        Toolsmith.ToolTinkering.TinkeringUtility.ReplaceBundle = false;

        var innerPlayer = (IServerPlayer)RuntimeHelpers.GetUninitializedObject(player.GetType());
        Reports.Clear();
        bench.Nested = () => bench.AttemptToCraft(innerPlayer);
        bench.AttemptToCraft(player);
        Check(Reports.Count == 2 && Reports[0].Player == innerPlayer && Reports[1].Player == player, "nested workbench restores outer attribution");
        Reports.Clear();
        bench.Nested = () => { try { bench.AttemptToCraft(innerPlayer, true); } catch (InvalidOperationException) { } };
        bench.AttemptToCraft(player);
        Check(Reports.Count == 1 && Reports[0].Player == player, "nested exception restores outer attribution");
        Toolsmith.ToolTinkering.TinkeringUtility.TryCraftToolFromSlots();
        Check(Reports.Count == 1, "nested calls leave no attribution after outer return");

        // Simulate unavailable attribution attachment, then retry output attachment.
        var strikeTarget = AccessTools.Method(typeof(Toolsmith.ToolTinkering.Blocks.BlockEntityWorkbench), "AttemptToCraft");
        var outputTarget = AccessTools.Method(typeof(Toolsmith.ToolTinkering.TinkeringUtility), "TryCraftToolFromSlots");
        adapter.Unpatch(strikeTarget, HarmonyPatchType.All, ToolsmithCompatSystem.HarmonyId);
        adapter.Unpatch(outputTarget, HarmonyPatchType.All, ToolsmithCompatSystem.HarmonyId);
        adapter.CreateClassProcessor(typeof(ToolsmithCompatSystem).GetNestedType("WorkbenchTool", BindingFlags.NonPublic)).Patch();
        Check(Harmony.GetPatchInfo(outputTarget)?.Owners.Contains(ToolsmithCompatSystem.HarmonyId) != true, "output attachment skipped when attribution hook is absent");
        bench.AttemptToCraft(player);
        Check(Reports.Count == 1, "missing attribution hook cannot credit output");
        var system = new ToolsmithCompatSystem();
        AccessTools.Field(typeof(ToolsmithCompatSystem), "harmony").SetValue(system, adapter);
        system.Dispose();
        bench.AttemptToCraft(player);
        Check(Reports.Count == 1 && !Harmony.HasAnyPatches(ToolsmithCompatSystem.HarmonyId), "dispose removes only adapter hooks");
        Check(Harmony.HasAnyPatches("questline.toolsmith.tests"), "adapter disposal preserves other Harmony owners");
        h.UnpatchAll("questline.toolsmith.tests");
        Console.WriteLine($"{checks} runtime checks passed");
    }
    sealed class DummySlot : ItemSlot { public DummySlot(ItemStack stack) : base(null) { Itemstack = stack; } }
}
namespace Toolsmith.ToolTinkering
{
    public static class TinkeringUtility
    {
        public static bool Empty, ReplaceBundle;
        [MethodImpl(MethodImplOptions.NoInlining)] public static void AssembleFullTool(ItemSlot bundleSlot, EntityAgent byEntity)
        {
            if (ReplaceBundle) bundleSlot.Itemstack = Program.Output();
        }
        [MethodImpl(MethodImplOptions.NoInlining)] public static ItemStack TryCraftToolFromSlots() => Empty ? null : Program.Output();
    }
}
namespace Toolsmith.ToolTinkering.Blocks
{
    public class BlockEntityWorkbench
    {
        public Action Nested;
        [MethodImpl(MethodImplOptions.NoInlining)] public void AttemptToCraft(IPlayer byPlayer, bool fail = false)
        {
            if (fail) throw new InvalidOperationException("synthetic provider failure");
            var nested = Nested;
            Nested = null;
            nested?.Invoke();
            Toolsmith.ToolTinkering.TinkeringUtility.TryCraftToolFromSlots();
        }
    }
}
