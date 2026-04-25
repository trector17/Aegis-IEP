#!/usr/bin/env python3
"""Render a dependency-free SVG preview for the generated surfer OBJ."""
from __future__ import annotations

from pathlib import Path
import math


def parse_obj(path: Path):
    verts = []
    faces = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("v "):
            _, x, y, z = line.split()[:4]
            verts.append((float(x), float(y), float(z)))
        elif line.startswith("f "):
            idx = [int(p.split("/")[0]) - 1 for p in line.split()[1:]]
            if len(idx) >= 3:
                faces.append(idx)
    return verts, faces


def rotate(v, ax=-28, ay=12):
    x, y, z = v
    rx = math.radians(ax)
    ry = math.radians(ay)

    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)

    # yaw around Y then pitch around X
    x1, y1, z1 = (x * cy + z * sy, y, -x * sy + z * cy)
    x2, y2, z2 = (x1, y1 * cx - z1 * sx, y1 * sx + z1 * cx)
    return x2, y2, z2


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    obj_path = root / "assets" / "3d" / "surfer_character.obj"
    out_path = root / "assets" / "3d" / "surfer_character_preview.svg"

    verts, faces = parse_obj(obj_path)
    rv = [rotate(v) for v in verts]

    xs = [v[0] for v in rv]
    ys = [v[1] for v in rv]
    zs = [v[2] for v in rv]

    w, h = 900, 900
    pad = 80
    sx = (w - 2 * pad) / (max(xs) - min(xs))
    sy = (h - 2 * pad) / (max(ys) - min(ys))
    s = min(sx, sy)

    def project(v):
        x, y, _ = v
        px = pad + (x - min(xs)) * s
        py = h - (pad + (y - min(ys)) * s)
        return px, py

    # painter's sort by average depth
    sorted_faces = sorted(faces, key=lambda f: sum(zs[i] for i in f) / len(f))

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#6b6b6b"/>',
    ]

    for face in sorted_faces:
        pts = [project(rv[i]) for i in face]
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        lines.append(f'<polygon points="{p}" fill="#c08960" stroke="#2a2a2a" stroke-opacity="0.10" stroke-width="0.6"/>')

    lines.append("</svg>")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
