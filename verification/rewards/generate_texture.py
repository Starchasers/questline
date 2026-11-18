"""Original Quest Cookie sprite, generated without external artwork (repository MIT license)."""
from pathlib import Path
import struct
import zlib

# Hand-authored 16x16 biscuit with chocolate chips and a small missing bite.
SPRITE = [
    "................", ".....oooooo.....", "...oohhhhhhoo...", "..ohhhhhhhhhho..",
    "..ohhccbhhhchho.", ".ohhhcbhhhchhho.", ".ohhhhhhhhhhho..", ".ohhchhcbhhhh...",
    ".ohhbhhcchh.....", ".ohhhhhhhhhho...", ".ohhhcchhhhhho..", "..ohhcbhhcccho..",
    "..ohhhhhhhbhho..", "...ooohhhhoo....", ".....oooooo.....", "................",
]
PALETTE = {".": (0, 0, 0, 0), "o": (130, 73, 36, 255), "h": (223, 167, 91, 255),
           "b": (164, 103, 52, 255), "c": (86, 47, 30, 255)}

def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

if __name__ == "__main__":
    assert len(SPRITE) == 16 and all(len(row) == 16 for row in SPRITE)
    raw = b"".join(b"\0" + bytes(v for pixel in row for v in PALETTE[pixel]) for row in SPRITE)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", 16, 16, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    path = Path(__file__).resolve().parents[2] / "questline/assets/questline/textures/item/questcookie.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)
    print(f"Generated original 16x16 RGBA sprite: {path} ({len(png)} bytes)")
