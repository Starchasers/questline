using System;
using System.Diagnostics;
using System.IO;

// Compatibility launcher only: no Cake or game assemblies are loaded.
var root = new DirectoryInfo(AppContext.BaseDirectory);
while (root != null && !File.Exists(Path.Combine(root.FullName, "tools", "packaging", "package.py")))
    root = root.Parent;
if (root == null)
{
    Console.Error.WriteLine("Cannot locate tools/packaging/package.py; use build.sh from the repository.");
    return 1;
}
var start = new ProcessStartInfo("python3") { UseShellExecute = false };
start.ArgumentList.Add(Path.Combine(root.FullName, "tools", "packaging", "package.py"));
foreach (var arg in args) start.ArgumentList.Add(arg);
using var process = Process.Start(start);
if (process == null) return 1;
process.WaitForExit();
return process.ExitCode;
