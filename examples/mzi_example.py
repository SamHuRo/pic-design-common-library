import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from picdesign import mzi_length_imbalance 

# Parameters
L1 = 100e-6      # 100 µm
L2 = 135e-6      # 135 µm
wavelength = 1.55e-6
n_eff = 2.4

# Compute MZI response
delta_L, delta_phi, fsr = mzi_length_imbalance.mzi_path_imbalance(
    L1=L1,
    L2=L2,
    wavelength=wavelength,
    n_eff=n_eff
)

print("Path-length imbalance:", delta_L, "m")
print("Phase difference:", delta_phi, "rad")
print("Approx FSR:", fsr, "m")