# pic-design-common-library

A common Python library of utilities for Photonic Integrated Circuit (**PIC**) design: analytical calculations for waveguides and resonators, helpers for exporting layouts to GDSII with [gdsfactory](https://gdsfactory.github.io/gdsfactory/), and FDTD simulation notebooks using [Tidy3D](https://www.flexcompute.com/tidy3d/).

Its goal is to centralize formulas and helpers that get reused across different photonic design projects, instead of rewriting them each time.

## Repository contents

```
pic-design-common-library/
├── picdesign/                  # Main library
│   ├── aprox_single_mode.py    # Single-mode condition (V-number criterion) for rectangular waveguides
│   ├── bend_loss_estimation.py # Fast bend-loss estimation
│   ├── conf_factor.py          # Optical confinement factor (Γ)
│   ├── fsr_calculation.py      # Free Spectral Range (FSR) of ring resonators
│   ├── gds_helper.py           # Export of gdsfactory components to GDSII + metadata
│   ├── lca.py                  # Simple Life Cycle Assessment (LCA) score
│   ├── materials.py            # Material/refractive-index definitions (in progress)
│   ├── mzi_length_imbalance.py # Length and phase imbalance in Mach-Zehnder interferometers
│   ├── prop_losses.py          # Propagation loss conversion (dB/cm ↔ 1/m)
│   ├── ring_circunference.py   # Ring geometry (radius ↔ circumference)
│   └── learning_chip/          # Learning chip with gdsfactory-based components
│       └── structures/         # Rings, spirals, and directional couplers
├── examples/                   # Example scripts using the library
├── fdtd/                       # FDTD simulation notebooks (Tidy3D)
├── docs/                       # Additional documentation
└── requirements.txt
```

> Note: some modules (`materials.py`, `learning_chip/`, `examples/waveguide_example.py`) are under active development and not fully implemented yet.

## Requirements

The project targets Python 3.10+ and mainly depends on:

- [`numpy`](https://numpy.org/) — numerical calculations in the `picdesign/` modules
- [`gdsfactory`](https://gdsfactory.github.io/gdsfactory/) — building and exporting GDSII layouts
- [`tidy3d`](https://www.flexcompute.com/tidy3d/), `gdstk`, `matplotlib`, `typeguard` — used in the `fdtd/` notebooks

`requirements.txt` is included in the repository but currently empty; install dependencies manually depending on which modules you plan to use:

```bash
pip install numpy gdsfactory
# For the FDTD notebooks:
pip install tidy3d gdstk matplotlib typeguard
```

## Installation

```bash
git clone https://github.com/SamHuRo/pic-design-common-library.git
cd pic-design-common-library
pip install -r requirements.txt  # or install dependencies manually (see above)
```

The library is not published on PyPI; it is used by importing it directly from the repository (see examples below).

## Usage

The scripts in `examples/` show how to add the root folder to `PYTHONPATH` and import the `picdesign` modules.

### Ring resonator geometry

```python
from picdesign import ring_circunference

radius, circumference = ring_circunference.ring_geometry(radius=10e-6)  # 10 µm
print("Radius (m):", radius)
print("Circumference (m):", circumference)
```

### Mach-Zehnder Interferometer (MZI) imbalance

```python
from picdesign import mzi_length_imbalance

delta_L, delta_phi, fsr = mzi_length_imbalance.mzi_path_imbalance(
    L1=100e-6,
    L2=135e-6,
    wavelength=1.55e-6,
    n_eff=2.4,
)

print("Path-length imbalance:", delta_L, "m")
print("Phase difference:", delta_phi, "rad")
print("Approx FSR:", fsr, "m")
```

### Life Cycle Assessment (LCA) score

```python
from picdesign import lca

score = lca.calculate_lca_score(
    co2_emissions=100,
    energy_consumption=500,
    water_usage=1000,
    waste_generation=50,
)

print(f"LCA Score: {score:.2f}")
```

You can run any of the example scripts directly:

```bash
python examples/ring_example.py
python examples/mzi_example.py
python examples/lca_example.py
```

## FDTD simulations

The `fdtd/` folder contains Jupyter notebooks that use Tidy3D to simulate photonic structures on an SOI (Silicon-on-Insulator) platform, including geometry and material definitions and guided-mode analysis. Running the simulations in the cloud requires a [Tidy3D](https://www.flexcompute.com/tidy3d/) account and credentials.

## Project status

This repository is under active development. The module APIs may change without notice.

## Author

Samuel Huertas Rojas ([@SamHuRo](https://github.com/SamHuRo))