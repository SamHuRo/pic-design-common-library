import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from picdesign import lca

score = lca.calculate_lca_score(
    co2_emissions=100,
    energy_consumption=500,
    water_usage=1000,
    waste_generation=50,
)

print(f"LCA Score: {score:.2f}")