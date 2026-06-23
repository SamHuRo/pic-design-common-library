from __future__ import annotations
import numpy as np


def estimate_bend_loss(
    radius: float,
    wavelength: float,
    n_core: float,
    n_clad: float,
    loss_coeff: float = 1e6,
    critical_radius: float | None = None,
    output: str = "dB_per_cm",
):
    """
    Description
    -----------
    Estimate waveguide bend loss using a simplified exponential model
    calibrated from effective-index contrast and bend radius.

    This is not a full Maxwell solver, but a fast design-level estimator
    for PIC routing and layout decisions.

    Inputs
    ------
    radius : float
        Bend radius.

    wavelength : float
        Operating wavelength.

    n_core : float
        Core refractive index.

    n_clad : float
        Cladding refractive index.

    loss_coeff : float
        Empirical scaling factor controlling loss severity.

    critical_radius : float, optional
        Radius below which bend loss increases rapidly.
        If None, it is estimated from index contrast.

    output : str
        "dB_per_cm" or "neper_per_m"

    Outputs
    -------
    loss : float
        Estimated bend loss.

    Units
    -----
    radius     : m
    wavelength : m
    loss       : dB/cm (default)

    Example
    -------
    >>> alpha = estimate_bend_loss(
    ...     radius=10e-6,
    ...     wavelength=1.55e-6,
    ...     n_core=2.4,
    ...     n_clad=1.44,
    ... )
    >>> print(alpha)
    """

    # Index contrast
    delta_n = n_core - n_clad

    # heuristic critical radius (very rough physics-based scaling)
    if critical_radius is None:
        critical_radius = wavelength / (2 * np.pi * np.sqrt(delta_n))

    # exponential radiation loss model
    loss_neper_per_m = loss_coeff * np.exp(-(radius - critical_radius) / critical_radius)

    # clamp stability
    loss_neper_per_m = np.maximum(loss_neper_per_m, 0.0)

    # convert to dB/cm if needed
    if output == "dB_per_cm":
        loss_db_per_m = 4.343 * loss_neper_per_m
        loss_db_per_cm = loss_db_per_m / 100
        return loss_db_per_cm

    return loss_neper_per_m