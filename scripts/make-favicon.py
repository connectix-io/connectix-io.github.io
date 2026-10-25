#!/usr/bin/env python3
"""Rasterise the Connectix mark into favicon.ico and apple-touch-icon.png.

Pure Python (zlib + struct): no Pillow, no cairo. The geometry is the mark's,
assets/images/connectix-mark.svg, on a 120x120 canvas:
  a circle (r 54) split left #BFE4E6 / right #8FCDD0,
  a cube with a #6B7280 top face and white 4px edges.

    python3 scripts/make-favicon.py
"""
import struct
import sys
import zlib
from pathlib import Path

LEFT = (0xBF, 0xE4, 0xE6)
RIGHT = (0x8F, 0xCD, 0xD0)
SLATE = (0x6B, 0x72, 0x80)
WHITE = (255, 255, 255)

TOP = [(60, 28), (88, 44), (60, 60), (32, 44)]
EDGES = [  # the white strokes, as segments on the 120 grid
    ((60, 28), (88, 44)), ((88, 44), (60, 60)), ((60, 60), (32, 44)), ((32, 44), (60, 28)),
    ((32, 44), (32, 78)), ((32, 78), (60, 94)), ((60, 94), (60, 60)),
    ((88, 44), (88, 78)), ((88, 78), (60, 94)),
]
STROKE = 4.0


def inside(poly, x, y):
    n = len(poly)
    hit = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                hit = not hit
    return hit


def seg_dist(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    cx, cy = ax + t * dx, ay + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5


def sample(x, y):
    """Colour and alpha at a point on the 120x120 canvas."""
    if (x - 60) ** 2 + (y - 60) ** 2 > 54 ** 2:
        return (0, 0, 0, 0)
    for a, b in EDGES:
        if seg_dist((x, y), a, b) <= STROKE / 2:
            return WHITE + (255,)
    if inside(TOP, x, y):
        return SLATE + (255,)
    return (LEFT if x < 60 else RIGHT) + (255,)


def render(size, ss=4):
    rows = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            r = g = b = a = 0
            for sy in range(ss):
                for sx in range(ss):
                    x = (px + (sx + 0.5) / ss) * 120 / size
                    y = (py + (sy + 0.5) / ss) * 120 / size
                    cr, cg, cb, ca = sample(x, y)
                    r += cr * ca
                    g += cg * ca
                    b += cb * ca
                    a += ca
            n = ss * ss
            if a:
                row += bytes((r // a, g // a, b // a, a // n))
            else:
                row += b"\0\0\0\0"
        rows.append(bytes(row))
    return rows


def png(size, rows):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = b"".join(b"\0" + r for r in rows)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def ico(images):
    """images: list of (size, png_bytes). PNG-in-ICO is read by every current browser."""
    head = struct.pack("<HHH", 0, 1, len(images))
    entries = b""
    data = b""
    offset = 6 + 16 * len(images)
    for size, blob in images:
        s = 0 if size >= 256 else size
        entries += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(blob), offset + len(data))
        data += blob
    return head + entries + data


def main():
    root = Path(__file__).resolve().parent.parent
    sizes = {s: png(s, render(s)) for s in (16, 32, 48)}
    (root / "favicon.ico").write_bytes(ico([(s, sizes[s]) for s in (16, 32, 48)]))
    (root / "apple-touch-icon.png").write_bytes(png(180, render(180, ss=2)))
    print("wrote favicon.ico (16, 32, 48) and apple-touch-icon.png (180)")


if __name__ == "__main__":
    sys.exit(main())
