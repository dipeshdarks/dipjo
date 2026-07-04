import winreg, sys, os

dipjo_dir = r"C:\Users\Lenovo\Downloads\Dipjo py"
bat_path = os.path.join(dipjo_dir, "run_dipjo.bat")
python_exe = sys.executable
main_py = os.path.join(dipjo_dir, "main.py")
icon_path = os.path.join(dipjo_dir, "website", "dipjo.ico")

bat_content = f'@echo off\r\n"{python_exe}" "{main_py}" "%~1"\r\npause\r\n'
with open(bat_path, "w") as f:
    f.write(bat_content)


keys = [
    (r"Software\Classes\.dipjo", [
        ("", "Dipjo.Script"),
        ("Content Type", "text/plain"),
        ("PerceivedType", "text"),
    ]),
    (r"Software\Classes\Dipjo.Script", [
        ("", "Dipjo Script File"),
    ]),
    (r"Software\Classes\Dipjo.Script\shell\open\command", [
        ("", f'"{bat_path}" "%1"'),
    ]),
    (r"Software\Classes\Dipjo.Script\DefaultIcon", [
        ("", icon_path),
    ]),
]

for key_path, values in keys:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        for name, data in values:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, data)
    print(f"Set: {key_path}")

import subprocess
subprocess.run(["cmd", "/c", "ie4uinit.exe", "-show"], capture_output=True)

print()
print("Done! .dipjo files should now:")
print("  - Show Dipjo icon")
print("  - Run when double-clicked")
print()
print("If not working:")
print("  1. Right-click hello.dipjo on Desktop")
print("  2. Click Open with > Choose another app")
print("  3. Click More apps > Look for another app")
print(f"  4. Browse to: {bat_path}")
print("  5. Check Always use this app")
