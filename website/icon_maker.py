"""
Dipjo Icon Creator - Pick your own colors!
Run: python icon_maker.py
"""
import struct
import os
import sys


def create_ico(filepath, bg_r, bg_g, bg_b, letter_color=(255,255,255)):
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
                r, g, b = bg_r, bg_g, bg_b
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
                    r, g, b = letter_color
                
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


PRESETS = {
    "1": ("Teal (default)", 0, 200, 180),
    "2": ("Red", 200, 50, 50),
    "3": ("Blue", 50, 100, 255),
    "4": ("Green", 50, 180, 50),
    "5": ("Purple", 150, 50, 200),
    "6": ("Orange", 255, 150, 0),
    "7": ("Pink", 255, 80, 150),
    "8": ("Gold", 255, 200, 0),
    "9": ("Custom (enter RGB)", None, None, None),
}

print("=" * 40)
print("  Dipjo Icon Maker")
print("=" * 40)
print()
print("Pick a background color:")
print()
for key, (name, r, g, b) in PRESETS.items():
    if r is not None:
        print(f"  {key}. {name} (rgb {r},{g},{b})")
    else:
        print(f"  {key}. {name}")
print()

choice = input("Enter number (1-9): ").strip()

if choice in PRESETS and PRESETS[choice][1] is not None:
    name, r, g, b = PRESETS[choice]
    print(f"\nUsing: {name}")
else:
    print("\nEnter RGB values (0-255):")
    r = int(input("  Red: "))
    g = int(input("  Green: "))
    b = int(input("  Blue: "))

ico_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dipjo.ico")
create_ico(ico_path, r, g, b)
print(f"\nIcon saved: {ico_path}")
print(f"Color: rgb({r}, {g}, {b})")

update = input("\nUpdate file association? (y/n): ").strip().lower()
if update == "y":
    try:
        import winreg
        icon_key = r"Software\Classes\Dipjo.Script\DefaultIcon"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, icon_key) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, ico_path)
        print("File association updated!")
    except Exception as e:
        print(f"Error: {e}")
