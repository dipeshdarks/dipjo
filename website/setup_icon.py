"""
Dipjo File Association Setup
Run this as Administrator to associate .dipjo files with Dipjo.
"""
import os
import sys
import ctypes
import struct
import winreg


def create_ico(filepath):
    """Create a simple .ico file with a 'D' letter icon."""
    width, height = 32, 32
    
    # Create a 32x32 RGBA image with a "D" shape
    pixels = []
    cx, cy = 16, 16
    
    for y in range(height):
        row = []
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            
            # Circle background (teal/cyan gradient)
            if dist <= 14:
                # Gradient from teal to purple
                t = dist / 14
                r = int(0 + t * 100)
                g = int(200 - t * 100)
                b = int(180 + t * 50)
                a = 255
                
                # Draw "D" letter
                in_d = False
                # Vertical line of D
                if -8 <= dx <= -5 and -7 <= dy <= 7:
                    in_d = True
                # Top horizontal
                if -8 <= dx <= -5 and -7 <= dy <= -5:
                    in_d = True
                # Bottom horizontal
                if -8 <= dx <= -5 and 5 <= dy <= 7:
                    in_d = True
                # Right curve
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
    
    # XOR mask (1 bit per pixel)
    xor_mask = bytes(width * height // 8)
    
    # AND mask (1 bit per pixel, all transparent except circle)
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
    
    # ICO file format
    # ICONDIR header
    ico_header = struct.pack('<HHH', 0, 1, 1)  # reserved, type=1(ICO), count=1
    
    # ICONDIRENTRY
    data_size = len(image_data) + len(and_mask)
    ico_entry = struct.pack('<BBBBHHII',
        width, height, 0, 0,  # width, height, colors, reserved
        1, 32,                # planes, bit count
        data_size,            # size of image data
        6 + 16                # offset (header + 1 entry)
    )
    
    # BITMAPINFOHEADER
    bmp_header = struct.pack('<IiiHHIIiiII',
        40,           # header size
        width,        # width
        height * 2,   # height (doubled for ICO format)
        1,            # planes
        32,           # bit count
        0,            # compression
        len(image_data) + len(and_mask),  # image size
        0, 0,         # pixels per meter
        0, 0          # colors
    )
    
    with open(filepath, 'wb') as f:
        f.write(ico_header)
        f.write(ico_entry)
        f.write(bmp_header)
        f.write(image_data)
        f.write(and_mask)
    
    return filepath


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def setup_file_association():
    """Set up Windows file association for .dipjo files."""
    
    dipjo_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(dipjo_dir, "main.py")
    icon_path = os.path.join(dipjo_dir, "dipjo.ico")
    
    # Create icon
    print("Creating icon...")
    create_ico(icon_path)
    print(f"  Icon created: {icon_path}")
    
    # Path to python
    python_exe = sys.executable
    
    # Registry paths
    ext_key = r"Software\Classes\.dipjo"
    prog_key = r"Software\Classes\Dipjo.Script"
    cmd_key = r"Software\Classes\Dipjo.Script\shell\open\command"
    icon_key = r"Software\Classes\Dipjo.Script\DefaultIcon"
    
    print("Setting up file association...")
    
    try:
        # .dipjo extension
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo.Script")
            winreg.SetValueEx(key, "Content Type", 0, winreg.REG_SZ, "text/plain")
        
        # Dipjo.Script class
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Dipjo Script File")
        
        # Command to run
        cmd = f'"{python_exe}" "{main.py}" "%1"'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
        
        # Icon
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, icon_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, icon_path)
        
        print("  Registry entries created successfully!")
        
        # Refresh Explorer icons
        import subprocess
        subprocess.run(["cmd", "/c", "ie4uinit.exe", "-show"], capture_output=True)
        
        print()
        print("Setup complete!")
        print(f"  .dipjo files will now use the Dipjo icon")
        print(f"  Double-clicking a .dipjo file will run it")
        print()
        
    except Exception as e:
        print(f"  Error: {e}")
        print("  Make sure you run this script as Administrator!")
        return False
    
    return True


if __name__ == "__main__":
    if not is_admin():
        print("This script needs Administrator privileges.")
        print("Right-click setup.bat and select 'Run as administrator'")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    setup_file_association()
    input("\nPress Enter to exit...")
