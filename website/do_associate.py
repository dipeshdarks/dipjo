import winreg, sys, os

ext_key = r"Software\Classes\.dipjo"
prog_key = r"Software\Classes\Dipjo.Script"
cmd_key = r"Software\Classes\Dipjo.Script\shell\open\command"
icon_key = r"Software\Classes\Dipjo.Script\DefaultIcon"

dipjo_dir = r"C:\Users\Lenovo\Downloads\Dipjo py"
main_py = os.path.join(dipjo_dir, "main.py")
icon_path = os.path.join(dipjo_dir, "website", "dipjo.ico")
python_exe = sys.executable

try:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo.Script")

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_key) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo Script File")

    cmd = f'"{python_exe}" "{main_py}" "%1"'
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, icon_key) as key:
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)

    print("File association created!")
    print(f"Extension: .dipjo")
    print(f"Program: {python_exe}")
    print(f"Script: {main_py}")
    print(f"Icon: {icon_path}")
except Exception as e:
    print(f"Error: {e}")
