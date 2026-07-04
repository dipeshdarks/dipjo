import winreg, sys, os

dipjo_dir = r"C:\Users\Lenovo\Downloads\Dipjo py"
bat_path = os.path.join(dipjo_dir, "run_dipjo.bat")
python_exe = sys.executable
main_py = os.path.join(dipjo_dir, "main.py")

bat_content = f'@echo off\r\n"{python_exe}" "{main_py}" "%~1"\r\npause\r\n'
with open(bat_path, "w") as f:
    f.write(bat_content)
print(f"Created: {bat_path}")

ext_key = r"Software\Classes\.dipjo"
cmd_key = r"Software\Classes\Dipjo.Script\shell\open\command"

with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key) as key:
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo.Script")

cmd = f'"{bat_path}" "%1"'
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key) as key:
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)

print(f"Association: .dipjo -> run_dipjo.bat")
print(f"Command: {cmd}")
print()
print("Now double-click any .dipjo file to run it!")
