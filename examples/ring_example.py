import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from picdesign import ring_circunference

R = 10e-6  # 10 µm radius

radius, circumference = ring_circunference.ring_geometry(radius=R)

print("Radius (m):", radius)
print("Circumference (m):", circumference)