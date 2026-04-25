#!/usr/bin/env python3
"""Generate a stylized 3D surfer character OBJ inspired by provided turnaround art."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math


@dataclass
class Mesh:
    name: str
    material: str
    vertices: list[tuple[float, float, float]]
    faces: list[tuple[int, ...]]


def box(center: tuple[float, float, float], size: tuple[float, float, float], name: str, material: str) -> Mesh:
    cx, cy, cz = center
    sx, sy, sz = size
    x = sx / 2
    y = sy / 2
    z = sz / 2
    verts = [
        (cx - x, cy - y, cz - z),
        (cx + x, cy - y, cz - z),
        (cx + x, cy + y, cz - z),
        (cx - x, cy + y, cz - z),
        (cx - x, cy - y, cz + z),
        (cx + x, cy - y, cz + z),
        (cx + x, cy + y, cz + z),
        (cx - x, cy + y, cz + z),
    ]
    faces = [
        (1, 2, 3, 4),
        (5, 8, 7, 6),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 8, 4),
        (5, 1, 4, 8),
    ]
    return Mesh(name, material, verts, faces)


def cylinder(
    center: tuple[float, float, float],
    radius: float,
    height: float,
    segments: int,
    axis: str,
    name: str,
    material: str,
) -> Mesh:
    cx, cy, cz = center
    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    h2 = height / 2

    for ring in (-h2, h2):
        for i in range(segments):
            a = (2 * math.pi * i) / segments
            c, s = math.cos(a), math.sin(a)
            if axis == "y":
                verts.append((cx + radius * c, cy + ring, cz + radius * s))
            elif axis == "x":
                verts.append((cx + ring, cy + radius * c, cz + radius * s))
            else:
                verts.append((cx + radius * c, cy + radius * s, cz + ring))

    # side quads
    for i in range(segments):
        n = (i + 1) % segments
        b0 = i + 1
        b1 = n + 1
        t1 = segments + n + 1
        t0 = segments + i + 1
        faces.append((b0, b1, t1, t0))

    # caps
    verts.append((cx, cy - h2, cz) if axis == "y" else ((cx - h2, cy, cz) if axis == "x" else (cx, cy, cz - h2)))
    verts.append((cx, cy + h2, cz) if axis == "y" else ((cx + h2, cy, cz) if axis == "x" else (cx, cy, cz + h2)))
    bottom_center = len(verts) - 1
    top_center = len(verts)

    for i in range(segments):
        n = (i + 1) % segments
        faces.append((bottom_center, n + 1, i + 1))
        faces.append((top_center, segments + i + 1, segments + n + 1))

    return Mesh(name, material, verts, faces)


def sphere(center: tuple[float, float, float], radius: float, rings: int, segments: int, name: str, material: str) -> Mesh:
    cx, cy, cz = center
    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for r in range(rings + 1):
        v = r / rings
        phi = math.pi * v
        y = radius * math.cos(phi)
        rr = radius * math.sin(phi)
        for s in range(segments):
            u = s / segments
            theta = 2 * math.pi * u
            x = rr * math.cos(theta)
            z = rr * math.sin(theta)
            verts.append((cx + x, cy + y, cz + z))

    for r in range(rings):
        for s in range(segments):
            n = (s + 1) % segments
            a = r * segments + s + 1
            b = r * segments + n + 1
            c = (r + 1) * segments + n + 1
            d = (r + 1) * segments + s + 1
            faces.append((a, b, c, d))

    return Mesh(name, material, verts, faces)


def write_obj(meshes: list[Mesh], obj_path: Path, mtl_name: str) -> None:
    lines = ["# Stylized surfer character", f"mtllib {mtl_name}"]
    vertex_offset = 0

    for mesh in meshes:
        lines.append(f"o {mesh.name}")
        lines.append(f"usemtl {mesh.material}")
        for v in mesh.vertices:
            lines.append(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}")
        for face in mesh.faces:
            shifted = [str(i + vertex_offset) for i in face]
            lines.append("f " + " ".join(shifted))
        vertex_offset += len(mesh.vertices)

    obj_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_mtl(mtl_path: Path) -> None:
    mats = {
        "skin": (0.76, 0.49, 0.30),
        "shorts": (0.09, 0.49, 0.45),
        "bandana": (0.05, 0.58, 0.62),
        "hair": (0.22, 0.13, 0.08),
        "beard": (0.18, 0.10, 0.06),
        "tooth": (0.95, 0.95, 0.88),
    }
    lines: list[str] = ["# Materials"]
    for name, kd in mats.items():
        lines.extend(
            [
                f"newmtl {name}",
                "Ka 0.050000 0.050000 0.050000",
                f"Kd {kd[0]:.6f} {kd[1]:.6f} {kd[2]:.6f}",
                "Ks 0.100000 0.100000 0.100000",
                "Ns 16.000000",
                "",
            ]
        )
    mtl_path.write_text("\n".join(lines), encoding="utf-8")


def build_character() -> list[Mesh]:
    meshes: list[Mesh] = []

    # Core body
    meshes.append(box((0, 1.32, 0), (0.52, 0.72, 0.30), "torso", "skin"))
    meshes.append(cylinder((0, 1.88, 0), 0.18, 0.20, 16, "y", "neck", "skin"))
    meshes.append(sphere((0, 2.18, 0), 0.24, 10, 16, "head", "skin"))

    # Beard volume
    meshes.append(cylinder((0, 2.00, 0.16), 0.12, 0.14, 12, "y", "beard", "beard"))

    # Arms
    for side in (-1, 1):
        sx = 0.36 * side
        meshes.append(cylinder((sx, 1.56, 0), 0.09, 0.46, 14, "y", f"upper_arm_{'l' if side < 0 else 'r'}", "skin"))
        meshes.append(cylinder((sx, 1.12, 0), 0.075, 0.44, 14, "y", f"forearm_{'l' if side < 0 else 'r'}", "skin"))
        meshes.append(sphere((sx, 0.86, 0.02), 0.08, 8, 12, f"hand_{'l' if side < 0 else 'r'}", "skin"))

    # Legs
    for side in (-1, 1):
        sx = 0.16 * side
        meshes.append(cylinder((sx, 0.66, 0), 0.11, 0.74, 16, "y", f"thigh_{'l' if side < 0 else 'r'}", "skin"))
        meshes.append(cylinder((sx, 0.22, 0), 0.09, 0.56, 16, "y", f"calf_{'l' if side < 0 else 'r'}", "skin"))
        meshes.append(box((sx, -0.08, 0.08), (0.18, 0.07, 0.36), f"foot_{'l' if side < 0 else 'r'}", "skin"))

    # Shorts
    meshes.append(box((0, 0.95, 0), (0.56, 0.32, 0.34), "shorts_waist", "shorts"))
    for side in (-1, 1):
        sx = 0.16 * side
        meshes.append(cylinder((sx, 0.78, 0), 0.13, 0.26, 16, "y", f"short_leg_{'l' if side < 0 else 'r'}", "shorts"))

    # Bandana
    meshes.append(cylinder((0, 2.24, 0), 0.245, 0.10, 16, "y", "bandana", "bandana"))

    # Dreadlocks (radial back strands)
    for i in range(11):
        a = math.radians(200 + i * 14)
        x = 0.19 * math.cos(a)
        z = 0.19 * math.sin(a)
        meshes.append(cylinder((x, 1.94, z), 0.028, 0.58, 8, "y", f"dread_{i}", "hair"))

    # Necklace and pendant
    meshes.append(cylinder((0, 1.82, 0.10), 0.015, 0.40, 12, "x", "necklace", "beard"))
    meshes.append(cylinder((0, 1.70, 0.22), 0.04, 0.10, 10, "y", "tooth_pendant", "tooth"))

    return meshes


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "assets" / "3d"
    out_dir.mkdir(parents=True, exist_ok=True)

    obj_path = out_dir / "surfer_character.obj"
    mtl_path = out_dir / "surfer_character.mtl"

    write_mtl(mtl_path)
    write_obj(build_character(), obj_path, mtl_path.name)

    print(f"Wrote {obj_path}")
    print(f"Wrote {mtl_path}")


if __name__ == "__main__":
    main()
