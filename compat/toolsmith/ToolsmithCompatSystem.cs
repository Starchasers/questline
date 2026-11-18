using System;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using questline;
using Vintagestory.API.Common;
using Vintagestory.API.Server;

namespace Questline.ToolsmithCompat;

/// <summary>Optional server-only adapter. No Toolsmith assembly reference is required.</summary>
public sealed class ToolsmithCompatSystem : ModSystem
{
    public const string HarmonyId = "com.dizzyd.questline.toolsmith";
    Harmony harmony;
    static QuestlineApi progress;

    public override bool ShouldLoad(EnumAppSide side) => side == EnumAppSide.Server;
    public override double ExecuteOrder() => 0.3;

    public override void StartServerSide(ICoreServerAPI api)
    {
        if (!api.ModLoader.IsModEnabled("toolsmith")) return;
        progress = api.ModLoader.GetModSystem<QuestlineApi>();
        harmony = new Harmony(HarmonyId);
        // Attribution must attach before the workbench output hook.
        foreach (var patch in new[] { typeof(InHand), typeof(WorkbenchStrike), typeof(WorkbenchTool) })
        {
            try { harmony.CreateClassProcessor(patch).Patch(); }
            catch (Exception e)
            {
                api.Logger.Warning("[questline-toolsmith] couldn't attach {0}: {1}", patch.Name, e.InnerException?.Message ?? e.Message);
            }
        }
    }

    public override void Dispose()
    {
        harmony?.UnpatchAll(HarmonyId);
        harmony = null;
        progress = null;
        WorkbenchStrike.Striking = null;
        base.Dispose();
    }

    static Type Utility => AccessTools.TypeByName("Toolsmith.ToolTinkering.TinkeringUtility");
    static Type Workbench => AccessTools.TypeByName("Toolsmith.ToolTinkering.Blocks.BlockEntityWorkbench");

    static void Credit(IPlayer player, ItemStack made)
    {
        if (player is IServerPlayer server && made?.Collectible?.Code != null)
            progress?.ReportCraft(server, made.Collectible.Code, made.StackSize);
    }

    [HarmonyPatch]
    static class InHand
    {
        static MethodBase TargetMethod() => AccessTools.Method(Utility, "AssembleFullTool");
        static void Prefix(ItemSlot bundleSlot, out ItemStack __state) => __state = bundleSlot.Itemstack;
        static void Postfix(ItemSlot bundleSlot, EntityAgent byEntity, ItemStack __state)
        {
            if (bundleSlot.Itemstack != __state && byEntity is EntityPlayer { Player: { } player })
                Credit(player, bundleSlot.Itemstack);
        }
    }

    [HarmonyPatch]
    static class WorkbenchStrike
    {
        [ThreadStatic] internal static IPlayer Striking;
        static MethodBase TargetMethod() => AccessTools.Method(Workbench, "AttemptToCraft");
        // Restore the previous scope even on an exception or nested workbench call.
        static void Prefix(IPlayer byPlayer, out IPlayer __state)
        {
            __state = Striking;
            Striking = byPlayer;
        }
        static void Finalizer(IPlayer __state) => Striking = __state;
    }

    [HarmonyPatch]
    static class WorkbenchTool
    {
        // Do not credit output if the attribution hook failed to attach.
        static bool Prepare() => Workbench != null && Utility != null
            && Harmony.GetPatchInfo(AccessTools.Method(Workbench, "AttemptToCraft"))?.Owners.Contains(HarmonyId) == true;
        static MethodBase TargetMethod() => AccessTools.Method(Utility, "TryCraftToolFromSlots");
        static void Postfix(ItemStack __result)
        {
            if (__result != null) Credit(WorkbenchStrike.Striking, __result);
        }
    }
}
