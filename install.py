"""
Dipjo Full Installer
Run this to install Dipjo on your computer.
"""
import os
import sys
import shutil
import winreg
import subprocess


def print_banner():
    print()
    print("=" * 50)
    print("   Dipjo Programming Language Installer")
    print("=" * 50)
    print()


def install():
    print_banner()

    # Install location
    install_dir = os.path.join(os.environ["USERPROFILE"], "Dipjo")
    print(f"Installing to: {install_dir}")
    print()

    # Create install directory
    os.makedirs(install_dir, exist_ok=True)
    os.makedirs(os.path.join(install_dir, "examples"), exist_ok=True)

    # Copy files
    source = os.path.dirname(os.path.abspath(__file__))

    files_to_copy = [
        "main.py", "ast_nodes.py", "lexer.py", "parser.py",
        "interpreter.py", "repl.py"
    ]

    print("Copying files...")
    for f in files_to_copy:
        src = os.path.join(source, f)
        dst = os.path.join(install_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  {f}")

    # Copy examples
    examples_dir = os.path.join(source, "examples")
    if os.path.exists(examples_dir):
        for f in os.listdir(examples_dir):
            if f.endswith(".dipjo"):
                src = os.path.join(examples_dir, f)
                dst = os.path.join(install_dir, "examples", f)
                shutil.copy2(src, dst)
                print(f"  examples/{f}")

    # Create run.bat
    python_exe = sys.executable
    bat_path = os.path.join(install_dir, "run_dipjo.bat")
    bat_content = f'@echo off\r\n"{python_exe}" "{os.path.join(install_dir, "main.py")}" "%~1"\r\n'
    with open(bat_path, "w") as f:
        f.write(bat_content)
    print(f"  run_dipjo.bat")

    # Create icon
    icon_path = os.path.join(install_dir, "dipjo.ico")
    create_ico(icon_path)
    print(f"  dipjo.ico")

    # Create desktop shortcut
    desktop = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Desktop")
    shortcut_bat = os.path.join(desktop, "Dipjo.bat")
    shortcut_content = f'@echo off\r\n"{python_exe}" "{os.path.join(install_dir, "main.py")}"\r\n'
    with open(shortcut_bat, "w") as f:
        f.write(shortcut_content)
    print(f"  Desktop shortcut: Dipjo.bat")

    # Create example on desktop
    example_dst = os.path.join(desktop, "hello.dipjo")
    example_src = os.path.join(install_dir, "examples", "welcome.dipjo")
    if os.path.exists(example_src):
        shutil.copy2(example_src, example_dst)
        print(f"  Desktop file: hello.dipjo")

    # Setup file association
    print()
    print("Setting up file association...")

    try:
        ext_key = r"Software\Classes\.dipjo"
        prog_key = r"Software\Classes\Dipjo.Script"
        cmd_key = r"Software\Classes\Dipjo.Script\shell\open\command"
        icon_key = r"Software\Classes\Dipjo.Script\DefaultIcon"

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo.Script")
            winreg.SetValueEx(key, "Content Type", 0, winreg.REG_SZ, "text/plain")

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo Script File")

        cmd = f'"{bat_path}" "%1"'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, icon_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)

        print("  File association: OK")

    except Exception as e:
        print(f"  Error: {e}")

    # Refresh icons
    try:
        subprocess.run(["cmd", "/c", "ie4uinit.exe", "-show"], capture_output=True)
    except:
        pass

    # Done
    print()
    print("=" * 50)
    print("  Installation Complete!")
    print("=" * 50)
    print()
    print("How to use:")
    print(f"  1. Double-click 'hello.dipjo' on Desktop")
    print(f"  2. Or double-click any .dipjo file")
    print(f"  3. Or open terminal and type:")
    print(f'     python "{os.path.join(install_dir, "main.py")}"')
    print()
    print(f"Installed to: {install_dir}")
    print()


def create_ico(filepath):
    """Create a simple .ico file."""
    import struct

    width, height = 32, 32
    pixels = []
    cx, cy = 16, 16

    for y in range(height):
        row = []
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = (dx*dx + dy*dy) ** 0.5

            if dist <= 14:
                t = dist / 14
                r = int(0 + t * 100)
                g = int(200 - t * 100)
                b = int(180 + t * 50)
                a = 255

                in_d = False
                if -8 <= dx <= -5 and -7 <= dy <= 7:
                    in_d = True
                if -8 <= dx <= -5 and -7 <= dy <= -5:
                    in_d = True
                if -8 <= dx <= -5 and 5 <= dy <= 7:
                    in_d = True
                if -5 <= dx <= 2 and -7 <= dy <= 7:
                    curve_dist = abs(dy)
                    if dx >= -5 - (7 - curve_dist) * 0.5:
                        in_d = True

                if in_d:
                    r, g, b = 255, 255, 255

                row.extend([b, g, r, a])
            else:
                row.extend([0, 0, 0, 0])

        pixels.append(bytes(row))

    image_data = b"".join(pixels)
    and_mask = bytearray(width * height // 8)
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            if dist > 14:
                byte_idx = (y * width + x) // 8
                bit_idx = (y * width + x) % 8
                and_mask[byte_idx] |= (1 << bit_idx)
    and_mask = bytes(and_mask)

    ico_header = struct.pack('<HHH', 0, 1, 1)
    data_size = len(image_data) + len(and_mask)
    ico_entry = struct.pack('<BBBBHHII', width, height, 0, 0, 1, 32, data_size, 6 + 16)
    bmp_header = struct.pack('<IiiHHIIiiII', 40, width, height * 2, 1, 32, 0, data_size, 0, 0, 0, 0)

    with open(filepath, 'wb') as f:
        f.write(ico_header)
        f.write(ico_entry)
        f.write(bmp_header)
        f.write(image_data)
        f.write(and_mask)


if __name__ == "__main__":
    install()
    input("Press Enter to exit...")
