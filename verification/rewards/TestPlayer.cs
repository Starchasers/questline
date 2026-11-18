using System.Reflection;
using System.Reflection.Emit;
using Vintagestory.API.Common;
using Vintagestory.API.Server;

// The SDK exposes an internal abstract IPlayer member, so neither a normal C# double
// nor DispatchProxy can implement it. Emit a no-op interface double with access checks
// disabled for this test-only assembly. This does not alter the SDK or game code.
public static class TestPlayer
{
    static readonly Type PlayerType = Build();
    public static IServerPlayer Create(string uid, IPlayerInventoryManager inventory)
    {
        var player = (IServerPlayer)Activator.CreateInstance(PlayerType);
        PlayerType.GetField("Uid").SetValue(player, uid);
        PlayerType.GetField("Inventory").SetValue(player, inventory);
        PlayerType.GetField("Entity").SetValue(player, new EntityPlayer());
        return player;
    }
    static Type Build()
    {
        var assembly = AssemblyBuilder.DefineDynamicAssembly(new AssemblyName("QuestCookiePlayerDouble"), AssemblyBuilderAccess.Run);
        assembly.SetCustomAttribute(new CustomAttributeBuilder(typeof(System.Runtime.CompilerServices.IgnoresAccessChecksToAttribute).GetConstructor([typeof(string)]), ["VintagestoryAPI"]));
        var type = assembly.DefineDynamicModule("Double").DefineType("Player", TypeAttributes.Public);
        type.AddInterfaceImplementation(typeof(IServerPlayer));
        var uid = type.DefineField("Uid", typeof(string), FieldAttributes.Public);
        var inventory = type.DefineField("Inventory", typeof(IPlayerInventoryManager), FieldAttributes.Public);
        var entity = type.DefineField("Entity", typeof(EntityPlayer), FieldAttributes.Public);
        foreach (var source in new[] { typeof(IServerPlayer) }.Concat(typeof(IServerPlayer).GetInterfaces())
            .SelectMany(t => t.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)))
        {
            var method = type.DefineMethod(source.Name, MethodAttributes.Public | MethodAttributes.Virtual | MethodAttributes.Final | MethodAttributes.NewSlot | MethodAttributes.HideBySig);
            var generic = source.IsGenericMethod ? method.DefineGenericParameters(source.GetGenericArguments().Select(t => t.Name).ToArray()) : [];
            Type Map(Type t) => t.IsGenericParameter ? generic[t.GenericParameterPosition] : t;
            Type result = Map(source.ReturnType);
            method.SetReturnType(result);
            method.SetParameters(source.GetParameters().Select(p => Map(p.ParameterType)).ToArray());
            var il = method.GetILGenerator();
            if (source.Name is "get_PlayerUID" or "get_PlayerName") { il.Emit(OpCodes.Ldarg_0); il.Emit(OpCodes.Ldfld, uid); }
            else if (source.Name == "get_InventoryManager") { il.Emit(OpCodes.Ldarg_0); il.Emit(OpCodes.Ldfld, inventory); }
            else if (source.Name == "get_Entity") { il.Emit(OpCodes.Ldarg_0); il.Emit(OpCodes.Ldfld, entity); }
            else if (source.Name == "get_ConnectionState") il.Emit(OpCodes.Ldc_I4, (int)EnumClientState.Playing);
            else if (result != typeof(void)) {
                var local = il.DeclareLocal(result); il.Emit(OpCodes.Ldloca, local); il.Emit(OpCodes.Initobj, result); il.Emit(OpCodes.Ldloc, local);
            }
            il.Emit(OpCodes.Ret);
            type.DefineMethodOverride(method, source);
        }
        return type.CreateType();
    }
}
