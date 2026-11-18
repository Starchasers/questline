namespace questline;

/// <summary>ModConfig/questline.json, read by the server at startup and on <c>/questline reload</c>.</summary>
public class QuestlineConfig
{
    public const string FileName = "questline.json";

    /// <summary>
    /// When a quest unlocks, credit it with what the player already did before: blocks broken,
    /// items crafted, creatures killed. Off means only work done while a quest is unlocked counts.
    /// </summary>
    public bool CreditEarlierWork = true;

    /// <summary>
    /// "open" (the default): every quest can be done from the start, in any order, and a quest's
    /// prerequisites only suggest an order. "strict": a quest stays locked until its prerequisite
    /// quests are done. Either way a quest still waits for a mod, a stage or a discovery it needs.
    /// </summary>
    public string Locking = OpenLocking;

    public const string OpenLocking = "open", StrictLocking = "strict";

    /// <summary>Whether prerequisite quests lock what comes after them; anything but "strict" leaves them open.</summary>
    public bool Strict => string.Equals(Locking, StrictLocking, System.StringComparison.OrdinalIgnoreCase);

    /// <summary>Players can form parties that share progress on party quests. Off, every party quest counts per player.</summary>
    public bool Parties = true;

    /// <summary>The asset domain chapters made in the editor belong to, and are exported under.</summary>
    public string EditorDomain = "questpack";

    /// <summary>
    /// The most the goal planner may show players: "guide" (every step and recipe), "hints" (the
    /// next things to get, not how) or "discovery" (no planner). Each player can choose less.
    /// </summary>
    public string RevealLevel = "hints";

    /// <summary>
    /// Legacy setting retained for configuration compatibility. This fork's cookie payout policy
    /// ignores rusty-gear multipliers; use ItemRewards to disable material rewards.
    /// </summary>
    public double GearRewards = 1;

    /// <summary>
    /// Quests give items. Off, they give none, choices included, for a server that uses the book
    /// to track progression: a quest with nothing left to give is done once its tasks are, with no
    /// claim, so items a quest would take in are kept. Stages are still granted, since later quests
    /// and other mods may need them, and a quest that grants one still takes its items at the claim.
    /// </summary>
    public bool ItemRewards = true;
}
