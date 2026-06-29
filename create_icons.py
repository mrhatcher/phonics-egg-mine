import struct, zlib, os, math

def write_png(path, size, bg, egg_fill, shine):
    cx, cy = size / 2, size * 0.52
    def px(x, y):
        dx, dy = x - cx, y - cy
        rx = size * 0.30
        ry = size * 0.38 if dy >= 0 else size * 0.30
        if (dx/rx)**2 + (dy/ry)**2 > 1.0:
            return bg
        sdx = x - (cx - size*0.09)
        sdy = y - (cy - size*0.11)
        if sdx**2 + sdy**2 <= (size*0.075)**2:
            return shine
        return egg_fill
    rows = [b'\x00' + b''.join(bytes(px(x,y)) for x in range(size)) for y in range(size)]
    raw = b''.join(rows)
    comp = zlib.compress(raw, 9)
    def chunk(n, d):
        c = n+d; return struct.pack('>I',len(d))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
    data = (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', comp)
            + chunk(b'IEND', b''))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    print(f'  {os.path.basename(path)}')

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
sky  = (91, 163, 232)
cream = (255, 248, 210)
white = (255, 255, 255)
for sz, name in [(180,'icon-180'),(192,'icon-192'),(512,'icon-512')]:
    write_png(os.path.join(base, f'{name}.png'), sz, sky, cream, white)
print('Icons ready.')
