using System.Reflection;
using questline;
using questline.Model;
using questline.Server;
using Vintagestory.API.Common;
using Vintagestory.API.Server;

/// <summary>Interface-only doubles around the real Claim implementation, not a game simulation.</summary>
public class Stub : DispatchProxy
{
    public System.Func<MethodInfo, object[], object> Handler;
    protected override object Invoke(MethodInfo method, object[] args)
    {
        var result = Handler?.Invoke(method, args);
        return result ?? (method.ReturnType.IsValueType && method.ReturnType != typeof(void)
            ? Activator.CreateInstance(method.ReturnType) : null);
    }
    public static T Make<T>(System.Func<MethodInfo, object[], object> handler = null) where T : class
    {
        T proxy = Create<T, Stub>(); ((Stub)(object)proxy).Handler = handler; return proxy;
    }
}

public sealed class ClaimSlot(InventoryBase inventory) : ItemSlot(inventory)
{
    public override void MarkDirty() { }
}

public sealed class ClaimFixture
{
    public QuestEngine Engine;
    public IServerPlayer A, B;
    public List<(string Code, int Count)> Given = [];
    public List<string> Lookups = [];
    public bool MissingCookie, InventoryFull;
    public Dictionary<string, byte[]> SaveData = [];
    public List<(string Code, int Count)> Dropped = [];
    public InventoryGeneric CarriedA = new(4, "hotbar", "a", null, (_, inv) => new ClaimSlot(inv));
    public InventoryGeneric CarriedB = new(4, "hotbar", "b", null, (_, inv) => new ClaimSlot(inv));
    public void Carry(string uid, string code, int count)
    {
        (uid == "a" ? CarriedA : CarriedB)[0].Itemstack = new ItemStack(new Item { Code = new AssetLocation(code), ItemId = 42, MaxStackSize = 64 }, count);
    }
    public ClaimFixture(QuestRegistry registry)
    {
        var item = new Item { Code = new AssetLocation(RewardPolicy.CookieCode), ItemId = 1234 };
        IPlayerInventoryManager Inventory(InventoryGeneric carried) => Stub.Make<IPlayerInventoryManager>((m, a) => {
            if (m.Name == "GetOwnInventory") return (string)a[0] == "hotbar" ? carried : null;
            if (m.Name == "TryGiveItemstack") {
                if (InventoryFull) return false;
                var stack = (ItemStack)a[0]; Given.Add((stack.Collectible.Code.ToString(), stack.StackSize)); stack.StackSize = 0; return true;
            }
            return null;
        });
        A = TestPlayer.Create("a", Inventory(CarriedA)); B = TestPlayer.Create("b", Inventory(CarriedB));
        var world = Stub.Make<IServerWorldAccessor>((m, a) => {
            if (m.Name == "get_AllOnlinePlayers") return new[] { A, B };
            if (m.Name == "PlayerByUid") return (string)a[0] == "a" ? A : B;
            if (m.Name == "GetItem") { Lookups.Add(a[0].ToString()); return !MissingCookie && a[0].ToString() == RewardPolicy.CookieCode ? item : null; }
            if (m.Name == "SpawnItemEntity") { var stack = (ItemStack)a[0]; Dropped.Add((stack.Collectible.Code.ToString(), stack.StackSize)); }
            return null;
        });
        var channel = Stub.Make<IServerNetworkChannel>();
        var network = Stub.Make<IServerNetworkAPI>((m, a) => m.Name == "RegisterChannel" ? channel : null);
        var events = Stub.Make<IServerEventAPI>();
        var logger = Stub.Make<ILogger>();
        var save = Stub.Make<ISaveGame>((m, a) => {
            if (m.Name == "GetData") return SaveData.GetValueOrDefault((string)a[0]);
            if (m.Name == "StoreData") SaveData[(string)a[0]] = (byte[])a[1];
            return null;
        });
        var manager = Stub.Make<IWorldManagerAPI>((m, _) => m.Name == "get_SaveGame" ? save : null);
        var api = Stub.Make<ICoreServerAPI>((m, a) => m.Name switch {
            "get_World" => world, "get_WorldManager" => manager, "get_Network" => network, "get_Event" => events, "get_Logger" => logger, _ => null
        });
        Engine = new QuestEngine(api);
        typeof(QuestEngine).GetField("channel", BindingFlags.Instance | BindingFlags.NonPublic).SetValue(Engine, channel);
        typeof(QuestEngine).GetProperty("Registry").SetValue(Engine, registry);
    }
    public void Complete(QuestDef quest, string uid)
    {
        var p = Engine.Holder(quest, uid).GetOrCreate(quest); p.Complete = true;
        for (int i = 0; i < p.Tasks.Length; i++) p.Tasks[i] = quest.Tasks[i].Count;
    }
}
