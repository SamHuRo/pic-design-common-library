import numpy as np


def estimate_confinement_factor(
    n_core: float,
    n_clad: float,
    wavelength: float,
    core_width: float,
    core_height: float,
    polarization: str = "TE",
):
    """
    Description
    -----------
    Estimate the optical confinement factor (Γ) of a rectangular
    integrated photonic waveguide using a simple effective-index
    approximation.

    The confinement factor represents the fraction of optical power
    confined in the core region:

        Γ ≈ Power_in_core / Total_power

    This model uses an analytical heuristic based on index contrast
    and mode decay into the cladding.

    Inputs
    ------
    n_core : float
        Refractive index of the waveguide core.

    n_clad : float
        Refractive index of the cladding.

    wavelength : float
        Operating wavelength (meters).

    core_width : float
        Width of the waveguide core (meters).

    core_height : float
        Height of the waveguide core (meters).

    polarization : str
        "TE" or "TM" mode polarization.

    Outputs
    -------
    gamma : float
        Estimated confinement factor (0 to 1).

    Units
    -----
    All geometric inputs are in meters.
    Refractive indices are dimensionless.
    Confinement factor is dimensionless.

    Example
    -------
    >>> gamma = estimate_confinement_factor(
    ...     n_core=2.4,
    ...     n_clad=1.44,
    ...     wavelength=1.55e-6,
    ...     core_width=500e-9,
    ...     core_height=220e-9,
    ... )
    >>> print(gamma)
    """

    # Index contrast
    delta_n = n_core - n_clad

    # Effective decay length approximation (very simplified)
    k0 = 2 * np.pi / wavelength

    # Field decay constant in cladding (heuristic)
    gamma_decay = k0 * np.sqrt(max(n_core**2 - n_clad**2, 1e-12))

    # Mode confinement scaling (geometry effect)
    geometry_factor = np.tanh(core_width * gamma_decay) * np.tanh(core_height * gamma_decay)

    # Normalize by index contrast influence
    index_factor = delta_n / n_core

    # Polarization correction (heuristic)
    if polarization.upper() == "TM":
        pol_factor = 0.85  # TM slightly less confined in high-index contrast systems
    else:
        pol_factor = 1.0

    # Final confinement factor (clipped to [0, 1])
    gamma = geometry_factor * index_factor * pol_factor
    gamma = float(np.clip(gamma, 0.0, 1.0))

    return gamma