#!/usr/bin/env python3
"""Generate a higher-fidelity stylized surfer character OBJ/MTL + preview render."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math


Vec3 = tuple[float, float, float]
Face = tuple[int, ...]


@dataclass
class Mesh:
    name: str
    material: str
    vertices: list[Vec3]
    faces: list[Face]


class Builder:
    def __init__(self) -> None:
        self.meshes: list[Mesh] = []

    def add(self, mesh: Mesh) -> None:
        self.meshes.append(mesh)


def translate(verts: list[Vec3], offset: Vec3) -> list[Vec3]:
    ox, oy, oz = offset
    return [(x + ox, y + oy, z + oz) for x, y, z in verts]


def rotate_x(verts: list[Vec3], deg: float) -> list[Vec3]:
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(x, y * c - z * s, y * s + z * c) for x, y, z in verts]


def rotate_z(verts: list[Vec3], deg: float) -> list[Vec3]:
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(x * c - y * s, x * s + y * c, z) for x, y, z in verts]


def uv_sphere(radius: float, rings: int, segments: int, name: str, material: str, center: Vec3 = (0, 0, 0)) -> Mesh:
    verts: list[Vec3] = []
    faces: list[Face] = []

    for r in range(rings + 1):
        v = r / rings
        phi = math.pi * v
        y = radius * math.cos(phi)
        rr = radius * math.sin(phi)
        for s in range(segments):
            u = s / segments
            t = 2 * math.pi * u
            verts.append((rr * math.cos(t), y, rr * math.sin(t)))

    for r in range(rings):
        for s in range(segments):
            n = (s + 1) % segments
            a = r * segments + s + 1
            b = r * segments + n + 1
            c = (r + 1) * segments + n + 1
            d = (r + 1) * segments + s + 1
            faces.append((a, b, c, d))

    return Mesh(name, material, translate(verts, center), faces)


def tapered_tube(profile: list[tuple[float, float]], segments: int, name: str, material: str, center: Vec3 = (0, 0, 0)) -> Mesh:
    """Build revolved mesh from (y, radius) profile."""
    verts: list[Vec3] = []
    faces: list[Face] = []

    for y, radius in profile:
        for i in range(segments):
            a = 2 * math.pi * i / segments
            verts.append((radius * math.cos(a), y, radius * math.sin(a)))

    rings = len(profile)
    for r in range(rings - 1):
        for i in range(segments):
            n = (i + 1) % segments
            a = r * segments + i + 1
            b = r * segments + n + 1
            c = (r + 1) * segments + n + 1
            d = (r + 1) * segments + i + 1
            faces.append((a, b, c, d))

    return Mesh(name, material, translate(verts, center), faces)


def capsule(radius: float, length: float, rings: int, segments: int, axis: str, name: str, material: str, center: Vec3) -> Mesh:
    h = max(0.0001, length / 2 - radius)
    profile: list[tuple[float, float]] = []

    for i in range(rings + 1):
        a = math.pi - (math.pi / 2) * (i / rings)
        profile.append((-h + radius * math.sin(a), radius * math.cos(a)))
    profile.append((h, radius))
    for i in range(1, rings + 1):
        a = (math.pi / 2) * (i / rings)
        profile.append((h + radius * math.sin(a), radius * math.cos(a)))

    mesh = tapered_tube(profile, segments, name, material)
    verts = mesh.vertices
    if axis == "x":
        verts = [(y, x, z) for x, y, z in verts]
    elif axis == "z":
        verts = [(x, z, y) for x, y, z in verts]

    mesh.vertices = translate(verts, center)
    return mesh


def write_obj(meshes: list[Mesh], obj_path: Path, mtl_name: str) -> None:
    lines = ["# Surfer character generated mesh", f"mtllib {mtl_name}"]
    voff = 0

    for mesh in meshes:
        lines += [f"o {mesh.name}", f"usemtl {mesh.material}"]
        lines += [f"v {x:.6f} {y:.6f} {z:.6f}" for x, y, z in mesh.vertices]
        for f in mesh.faces:
            lines.append("f " + " ".join(str(i + voff) for i in f))
        voff += len(mesh.vertices)

    obj_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_mtl(path: Path) -> None:
    mats = {
        "skin": (0.74, 0.49, 0.31),
        "hair": (0.22, 0.14, 0.08),
        "beard": (0.17, 0.10, 0.06),
        "shorts_base": (0.07, 0.46, 0.45),
        "shorts_accent": (0.92, 0.68, 0.17),
        "bandana": (0.07, 0.56, 0.62),
        "tooth": (0.96, 0.94, 0.86),
        "cord": (0.10, 0.08, 0.07),
    }
    lines: list[str] = ["# Surfer materials"]
    for name, (r, g, b) in mats.items():
        lines += [
            f"newmtl {name}",
            "Ka 0.06 0.06 0.06",
            f"Kd {r:.6f} {g:.6f} {b:.6f}",
            "Ks 0.120000 0.120000 0.120000",
            "Ns 20.0",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build_character() -> list[Mesh]:
    b = Builder()

    torso_profile = [
        (0.00, 0.22), (0.10, 0.24), (0.25, 0.25), (0.45, 0.24),
        (0.64, 0.22), (0.82, 0.19), (0.95, 0.16),
    ]
    b.add(tapered_tube(torso_profile, 36, "torso", "skin", center=(0.0, 1.00, 0.0)))
    b.add(capsule(0.10, 0.20, 6, 24, "y", "neck", "skin", (0.0, 1.98, 0.0)))
    b.add(uv_sphere(0.23, 16, 30, "head", "skin", center=(0.0, 2.25, 0.0)))

    # chest/abs definition (subtle overlay)
    for y, r, n in [(1.37, 0.08, "pec_l"), (1.37, 0.08, "pec_r"), (1.20, 0.05, "abs1"), (1.08, 0.05, "abs2")]:
        x = -0.11 if n.endswith("l") else (0.11 if n.endswith("r") else 0.0)
        b.add(capsule(r, 0.03, 4, 18, "x", n, "skin", (x, y, 0.18)))

    # legs
    for side in (-1, 1):
        sx = 0.13 * side
        b.add(capsule(0.105, 0.74, 8, 24, "y", f"thigh_{side}", "skin", (sx, 0.63, 0.0)))
        b.add(capsule(0.085, 0.60, 8, 24, "y", f"calf_{side}", "skin", (sx, 0.18, -0.01)))
        foot = capsule(0.065, 0.30, 6, 20, "z", f"foot_{side}", "skin", (sx, -0.13, 0.12))
        foot.vertices = rotate_x(foot.vertices, -8)
        b.add(foot)

    # arms in relaxed A-pose
    for side in (-1, 1):
        sx = 0.33 * side
        upper = capsule(0.085, 0.49, 8, 22, "y", f"upper_arm_{side}", "skin", (sx, 1.50, 0.0))
        upper.vertices = rotate_z(upper.vertices, -12 * side)
        b.add(upper)
        fore = capsule(0.072, 0.44, 8, 22, "y", f"forearm_{side}", "skin", (0.38 * side, 1.08, 0.02))
        fore.vertices = rotate_z(fore.vertices, -9 * side)
        b.add(fore)
        b.add(uv_sphere(0.082, 10, 18, f"hand_{side}", "skin", center=(0.43 * side, 0.83, 0.04)))

    # shorts with color blocks
    shorts = tapered_tube([(0.00, 0.27), (0.16, 0.28), (0.30, 0.26), (0.42, 0.24)], 36, "shorts", "shorts_base", center=(0.0, 0.78, 0.0))
    b.add(shorts)
    for side in (-1, 1):
        b.add(capsule(0.12, 0.24, 6, 22, "y", f"short_leg_{side}", "shorts_base", (0.14 * side, 0.63, 0.0)))

    # decorative shorts accents (flower-ish discs)
    accents = [(-0.10, 0.82, 0.19), (0.08, 0.86, -0.18), (-0.18, 0.71, -0.06), (0.18, 0.76, 0.08)]
    for i, c in enumerate(accents):
        b.add(capsule(0.04, 0.01, 3, 14, "z", f"short_accent_{i}", "shorts_accent", c))

    # hair band and beard
    b.add(capsule(0.23, 0.08, 5, 30, "y", "bandana", "bandana", (0.0, 2.28, 0.0)))
    beard = capsule(0.11, 0.18, 6, 20, "y", "beard", "beard", (0.0, 2.04, 0.15))
    beard.vertices = rotate_x(beard.vertices, 10)
    b.add(beard)

    # dreadlocks arranged around back scalp
    for i in range(14):
        ang = math.radians(160 + i * 14)
        x = 0.18 * math.cos(ang)
        z = 0.18 * math.sin(ang)
        y = 2.18 + 0.02 * math.sin(i)
        dread = capsule(0.022, 0.56 + 0.04 * math.sin(i * 0.8), 4, 10, "y", f"dread_{i}", "hair", (x, y - 0.27, z))
        dread.vertices = rotate_x(dread.vertices, 8)
        b.add(dread)

    # necklace + pendant tooth
    b.add(capsule(0.012, 0.42, 4, 16, "x", "necklace", "cord", (0.0, 1.84, 0.10)))
    pend = capsule(0.036, 0.12, 5, 14, "y", "pendant", "tooth", (0.0, 1.70, 0.22))
    pend.vertices = rotate_x(pend.vertices, -8)
    b.add(pend)

    return b.meshes


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "assets" / "3d"
    out.mkdir(parents=True, exist_ok=True)

    obj = out / "surfer_character.obj"
    mtl = out / "surfer_character.mtl"

    write_mtl(mtl)
    write_obj(build_character(), obj, mtl.name)

    print(f"Wrote {obj}")
    print(f"Wrote {mtl}")


if __name__ == "__main__":
    main()
