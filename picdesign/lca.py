def calculate_lca_score(
    co2_emissions,
    energy_consumption,
    water_usage,
    waste_generation,
    weights=None,
):
    """
    Description
    -----------
    Calculate a simple Life Cycle Assessment (LCA) score using
    weighted environmental impact indicators.

    Inputs
    ------
    co2_emissions : float
        Total greenhouse gas emissions.

    energy_consumption : float
        Total energy consumed.

    water_usage : float
        Total water used.

    waste_generation : float
        Total waste generated.

    weights : dict, optional
        Weighting factors for each category.
        Default:
        {
            "co2": 0.4,
            "energy": 0.3,
            "water": 0.2,
            "waste": 0.1,
        }

    Outputs
    -------
    score : float
        Overall environmental impact score.
        Lower values indicate lower environmental impact.

    Units
    -----
    co2_emissions      : kg CO₂-eq
    energy_consumption : kWh
    water_usage        : L
    waste_generation   : kg
    score              : arbitrary units

    Example
    -------
    >>> score = calculate_lca_score(
    ...     co2_emissions=100,
    ...     energy_consumption=500,
    ...     water_usage=1000,
    ...     waste_generation=50,
    ... )
    >>> print(score)
    """

    if weights is None:
        weights = {
            "co2": 0.4,
            "energy": 0.3,
            "water": 0.2,
            "waste": 0.1,
        }

    score = (
        weights["co2"] * co2_emissions
        + weights["energy"] * energy_consumption
        + weights["water"] * water_usage
        + weights["waste"] * waste_generation
    )

    return score