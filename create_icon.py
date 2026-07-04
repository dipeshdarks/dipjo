"""
Create Dipjo Icon - Blue/Purple gradient D with pen nib
"""
import struct
import os


def create_dipjo_icon(filepath, size=64):
    """Create a professional Dipjo icon with blue/purple gradient."""
    width, height = size, size
    pixels = []
    cx, cy = size // 2, size // 2
    radius = size // 2 - 2

    for y in range(height):
        row = []
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dy - x - cx 
            dist = (dx*dx + dy*dy) ** 0.5

            if dist <= radius:
                # Blue/Purple gradient background
                t = dist / radius
                angle = (dx + dy) / (size * 0.7)
                r = int(30 + t * 80 + angle * 40)
                g = int(50 + (1-t) * 100)
                b = int(180 + t * 50 - angle * 30)
                a = 255
                

                # Dark border
                if dist > radius - 2:
                    r, g, b = 20, 20, 60

                # Draw stylized "D"
                in_d = False

                # Left vertical bar
                if -radius*0.55 <= dx <= -radius*0.35 and -radius*0.5 <= dy <= radius*0.5:
                    in_d = True

                # Top bar
                if -radius*0.55 <= dx <= -radius*0.1 and -radius*0.5 <= dy <= -radius*0.35:
                    in_d = True

                # Bottom bar
                if -radius*0.55 <= dx <= -radius*0.1 and radius*0.35 <= dy <= radius*0.5:
                    in_d = True

                # Right curve
                if -radius*0.35 <= dx <= radius*0.35:
                    curve_y = abs(dy)
                    curve_limit = radius * 0.5 * (1 - (dx / (radius * 0.7)) ** 2)
                    if curve_y <= curve_limit and dx >= -radius*0.1:
                        in_d = True

                # Pen nib (top right)
                pen_cx = radius * 0.45
                pen_cy = -radius * 0.55
                pen_dx = x - pen_cx
                pen_dy = y - pen_cy
                pen_dist = (pen_dx*pen_dx + pen_dy*pen_dy) ** 0.5

                # Pen body
                if pen_dist <= radius * 0.18:
                    in_d = True
                    # Pen tip highlight
                    if pen_dist <= radius * 0.08:
                        r, g, b = 100, 200, 255

                # Pen nib shape (triangle pointing down-right)
                if 0 <= pen_dx <= radius * 0.25:
                    if -pen_dx * 0.8 <= pen_dy <= pen_dx * 0.8:
                        in_d = True

                if in_d:
                    # White/light color for the D
                    if pen_dist <= radius * 0.18:
                        r, g, b = 100, 200, 255
                    else:
                        r, g, b = 220, 230, 255

                row.extend([b, g, r, a])
            else:
                row.extend([0, 0, 0, 0])

        pixels.append(bytes(row))

    image_data = b"".join(pixels)

    # AND mask
    and_mask = bytearray(width * height // 8)
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            if dist > radius:
                byte_idx = (y * width + x) // 8
                bit_idx = (y * width + x) % 8
                and_mask[byte_idx] |= (1 << bit_idx)
    and_mask = bytes(and_mask)

    # ICO format
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

    return filepath


# Create multiple sizes for ICO
base = r'C:\Users\Lenovo\Downloads\Dipjo py'
icon_dir = os.path.join(base, '.vscode', 'dipjo-extension', 'icons')
os.makedirs(icon_dir, exist_ok=True)

# Create 16x16, 32x32, 48x48, 64x64 icons
sizes = [16, 32, 48, 64]
icon_files = []

for s in sizes:
    path = os.path.join(icon_dir, f'dipjo_{s}.ico')
    create_dipjo_icon(path, s)
    icon_files.append(path)
    print(f'Created: dipjo_{s}.ico')

# Create main icon (multi-size)
main_icon = os.path.join(icon_dir, 'dipjo.ico')
create_dipjo_icon(main_icon, 64)
print(f'Created: dipjo.ico')

# Also copy to main locations
import shutil
targets = [
    os.path.join(base, 'dipjo.ico'),
    os.path.join(base, 'website', 'dipjo.ico'),
    os.path.join(os.environ['USERPROFILE'], 'Dipjo', 'dipjo.ico'),
]

for target in targets:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(main_icon, target)
    print(f'Copied to: {target}')

print()
print('All icons created!')
