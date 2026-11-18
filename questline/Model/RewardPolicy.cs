using System.Collections.Generic;
using System.Linq;

namespace questline.Model;

/// <summary>
/// The fork's material-payout boundary. Authored resources remain source metadata, not
/// permission to mint those resources. One material reward per list becomes one tiny
/// cookie; redundant item-only choices disappear. Stages and stage-bearing choices stay.
/// </summary>
public static class RewardPolicy
{
    public const string CookieCode = "questline:questcookie";

    /// <summary>Validate the authored tree before normalization or opt-out can hide errors.
    /// The claim protocol has one pick per top-level choice; nested choices are unsupported.</summary>
    public static IEnumerable<string> Errors(IEnumerable<RewardDef> authored, bool inChoice = false)
    {
        if (authored == null) { yield return "reward list is null"; yield break; }
        foreach (var reward in authored)
        {
            if (reward == null) { yield return "reward is null"; continue; }
            switch (reward.Type)
            {
                case "item":
                    break; // Authored material metadata is never dispatched; normalization replaces it.
                case "stage":
                    if (string.IsNullOrWhiteSpace(reward.Stage)) yield return "stage reward names no stage";
                    break;
                case "choice":
                    if (inChoice) yield return "nested choice rewards are unsupported";
                    if (reward.Options == null || reward.Options.Count == 0) yield return "choice reward has no options";
                    else foreach (var error in Errors(reward.Options, true)) yield return error;
                    break;
                default:
                    yield return $"unknown reward type '{reward.Type}'";
                    break;
            }
        }
    }

    public static List<RewardDef> Apply(IEnumerable<RewardDef> authored, bool items = true)
    {
        // Materialize once so one-shot enumerables have the same validation and projection.
        var source = authored?.ToList();
        var error = Errors(source).FirstOrDefault();
        if (error != null) throw new System.ArgumentException(error, nameof(authored));
        return Normalize(source, items);
    }

    static List<RewardDef> Normalize(IEnumerable<RewardDef> authored, bool items)
    {
        var result = new List<RewardDef>();
        bool hasCookie = false;
        foreach (var reward in authored)
        {
            var effective = reward;
            if (reward.Type == "choice")
            {
                var options = Normalize(reward.Options, items);
                if (options.Count == 0) continue;
                effective = options.All(r => r.Type == "item")
                    ? Cookie()
                    : new RewardDef { Type = "choice", Options = options };
            }
            if (effective.Type == "item")
            {
                if (!items || hasCookie) continue;
                effective = Cookie();
                hasCookie = true;
            }
            result.Add(effective);
        }
        return result;
    }

    static RewardDef Cookie() => new() { Type = "item", Item = CookieCode, Count = 1 };
}
