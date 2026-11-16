using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using questline.Model;
using questline.Server;
using Vintagestory.API.Client;
using Vintagestory.API.Common;
using Vintagestory.API.Config;
using Vintagestory.API.Util;

namespace questline.Client;

/// <summary>Player-facing words for quests: titles, task lines, reward names and requirements.</summary>
public class QuestText(ICoreClientAPI capi, QuestClient client)
{
    /// <summary>A lang entry. The editor's own text, sent with the definitions, comes first.</summary>
    public string Get(string key) => client.Registry?.Text.TryGetValue(key, out var value) == true ? value : Lang.Get(key);

    public bool Has(string key) => client.Registry?.Text.ContainsKey(key) == true || Translations.Has(key);

    public string Title(string questId) => Get(questId + "-title");

    public string Description(string questId) => Has(questId + "-desc") ? Get(questId + "-desc") : null;

    public string ChapterTitle(string chapterId) => Get(chapterId + "-title");

    public string QuestlineTitle(string questlineId) => Lang.Get(questlineId + "-title");

    public string State(QuestState state) => Lang.Get("questline:state-" + state.ToString().ToLowerInvariant());

    /// <summary>
    /// A stack standing for a task or reward code: the item itself, a regular expression's first
    /// choice, or else the first match in the game's own order.
    /// </summary>
    public ItemStack StackFor(string code, int size = 1)
    {
        if (code == null) return null;
        var loc = new AssetLocation(code);
        // "Anything at all" has no one item that stands for it.
        if (loc.Path == "*") return null;
        CollectibleObject collectible = Collectible(loc) ?? (FirstChoice(loc) is { } first ? Collectible(first) : null);
        collectible ??= capi.World.Collectibles.FirstOrDefault(c => c.Code != null && WildcardUtil.Match(loc, c.Code));
        return collectible == null ? null : new ItemStack(collectible, size);
    }

    CollectibleObject Collectible(AssetLocation loc) => capi.World.GetItem(loc) ?? (CollectibleObject)capi.World.GetBlock(loc);

    static readonly Regex Choices = new(@"\(([^()|]*)(?:\|[^()]*)?\)");

    /// <summary>
    /// The item a regular expression names first: game:@axe-(flint|chert|granite) is a flint axe. The
    /// game's own order would pick chert, its first variant, for every stone tool. Null for anything
    /// that isn't a plain choice between alternatives.
    /// </summary>
    static AssetLocation FirstChoice(AssetLocation loc)
    {
        if (!loc.Path.StartsWith('@')) return null;
        string path = Choices.Replace(loc.Path[1..], "$1");
        return path.IndexOfAny(['(', ')', '|', '*', '+', '?', '.', '[', '\\', '^', '$', '{']) < 0 ? new AssetLocation(loc.Domain, path) : null;
    }

    /// <summary>A stage or custom key's own lang entry (<c>&lt;name&gt;-title</c>) if it has one, or the name itself.</summary>
    string Named(string name) => Has(name + "-title") ? Get(name + "-title") : name;

    public string TaskLine(TaskDef task)
    {
        if (task.Type == "checkbox") return Lang.Get("questline:task-checkbox");
        if (task.Type == "custom") return Named(task.Key);
        if (task.Type == "visit") return Lang.Get("questline:task-visit", Get(TaskDef.StructureNameKey(task.Structure)));
        return Lang.Get("questline:task-" + task.Type, TargetName(task));
    }

    string TargetName(TaskDef task)
    {
        bool wildcard = TaskDef.IsPattern(task.Target);
        if (task.OnEntity)
        {
            // Creatures are named by their spawn item, item-creature-<code>. A wildcard such as
            // chicken-* is named by what comes before the star: a first match would say "Rooster".
            var loc = new AssetLocation(task.Target);
            if (wildcard && !loc.Path.Contains('*'))
            {
                // A regular expression: named by the first creature it matches.
                var first = capi.World.EntityTypes.FirstOrDefault(e => WildcardUtil.Match(loc, e.Code));
                return first == null ? task.Target : Lang.Get("questline:any-of", Lang.Get(first.Code.Domain + ":item-creature-" + first.Code.Path));
            }
            if (wildcard)
            {
                string prefix = loc.Path[..loc.Path.IndexOf('*')].TrimEnd('-');
                string key = loc.Domain + ":item-creature-" + prefix;
                string kind = Translations.Has(key) ? Lang.Get(key) : prefix.Replace('-', ' ');
                return Lang.Get("questline:any-of", kind);
            }
            return capi.World.EntityTypes.Any(e => e.Code.Equals(loc)) ? Lang.Get(loc.Domain + ":item-creature-" + loc.Path) : task.Target;
        }

        if (task.Name != null) return Get(task.Name);
        if (wildcard && SharedName(task.Target) is { } shared) return Lang.Get("questline:any-of", shared);
        var stack = StackFor(task.Target);
        if (stack == null) return task.Target;
        string name = stack.GetName();
        return wildcard ? Lang.Get("questline:any-of", name) : name;
    }

    readonly Dictionary<string, string> sharedNames = [];

    /// <summary>
    /// What every item a pattern matches is called, in the player's language: the one name they
    /// share once each drops its bracketed variant ("Hand basket (reed)"), or else the words every
    /// name has ("Chert axe head", "Flint axe head": "axe head"). Null when they have nothing in
    /// common, as fruit don't; a task names those itself. Items with no name of their own (the
    /// game shows their lang key) are left out.
    /// </summary>
    public string SharedName(string pattern)
    {
        if (sharedNames.TryGetValue(pattern, out var cached)) return cached;
        var loc = new AssetLocation(pattern);
        var names = capi.World.Collectibles
            .Where(c => c.Code != null && WildcardUtil.Match(loc, c.Code))
            .Select(c => new ItemStack(c).GetName())
            .Where(n => !string.IsNullOrWhiteSpace(n) && !Untranslated.IsMatch(n))
            .Select(BaseName).Distinct().ToList();
        string shared = names.Count switch
        {
            0 => null,
            1 => names[0],
            _ => CommonWords(names),
        };
        return sharedNames[pattern] = string.IsNullOrWhiteSpace(shared) ? null : shared;
    }

    static readonly Regex Untranslated = new(@"^[a-z0-9_-]+:(block|item)-");
    static readonly Regex VariantSuffix = new(@"\s*\([^()]*\)\s*$");

    /// <summary>"Egg basket (walnut)" as "Egg basket": an item's name without its variant. Names that are nothing but a bracket stay whole.</summary>
    internal static string BaseName(string name)
    {
        string stripped = name;
        while (VariantSuffix.Match(stripped) is { Success: true } m && m.Index > 0) stripped = stripped[..m.Index];
        return stripped;
    }

    /// <summary>The first name's words that every other name has too, in its order.</summary>
    static string CommonWords(List<string> names)
    {
        var others = names.Skip(1).Select(n => n.ToLowerInvariant().Split(' ', StringSplitOptions.RemoveEmptyEntries).ToHashSet()).ToList();
        return string.Join(" ", names[0].Split(' ', StringSplitOptions.RemoveEmptyEntries).Where(w => others.All(o => o.Contains(w.ToLowerInvariant()))));
    }

    public string RewardLine(RewardDef reward)
    {
        if (reward.Type == "stage") return Lang.Get("questline:reward-stage", Named(reward.Stage));
        var stack = StackFor(reward.Item, reward.Count);
        return $"{reward.Count}× {stack?.GetName() ?? reward.Item}";
    }

    /// <summary>A requirement in words: "Gather flint and (Dig in or Lay a stone)".</summary>
    public string Describe(Requirement r, bool nested = false)
    {
        string text = r switch
        {
            QuestRequirement q => client.Registry?.Get(q.QuestId) != null ? Title(q.QuestId) : q.QuestId,
            ModRequirement m => Lang.Get("questline:req-mod", m.ModId),
            StageRequirement s => Lang.Get("questline:req-stage", Named(s.Stage)),
            ChapterCompleteRequirement c => Lang.Get("questline:req-chapter", ChapterTitle(c.ChapterId)),
            DiscoveredRequirement => Lang.Get("questline:req-discovered"),
            AllRequirement a => string.Join(Lang.Get("questline:req-and"), a.Of.Select(x => Describe(x, true))),
            AnyRequirement a => string.Join(Lang.Get("questline:req-or"), a.Of.Select(x => Describe(x, true))),
            AtLeastRequirement a => Lang.Get("questline:req-atleast", a.N, string.Join(", ", a.Of.Select(x => Describe(x, true)))),
            _ => "?",
        };
        return nested && r is CompositeRequirement { Of.Count: > 1 } ? $"({text})" : text;
    }
}
