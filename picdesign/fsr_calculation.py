from __future__ import annotations
import numpy as np


def calculate_fsr_ring(
    wavelength: float,
    n_eff: float,
    radius: float,
    dn_eff_dlambda: float | None = None,
    use_group_index: bool = True,
):
    """
    Description
    -----------
    Compute the Free Spectral Range (FSR) of a ring resonator using an
    effective-index-based approximation. Optionally includes dispersion
    correction via dn_eff/dλ to estimate the group index.

    Inputs
    ------
    wavelength : float
        Operating wavelength.

    n_eff : float
        Effective refractive index of the waveguide mode.

    radius : float
        Ring radius.

    dn_eff_dlambda : float, optional
        Derivative of effective index with respect to wavelength.
        Used to compute group index:
        n_g = n_eff - λ * dn_eff/dλ

    use_group_index : bool
        If True, uses group index approximation.
        If False, uses n_eff directly.

    Outputs
    -------
    fsr_lambda : float
        Free spectral range in wavelength units.

    fsr_freq : float
        Free spectral range in frequency units (Hz).

    Units
    -----
    wavelength : m
    radius     : m
    fsr_lambda : m
    fsr_freq   : Hz

    Example
    -------
    >>> fsr_l, fsr_f = calculate_fsr_ring(
    ...     wavelength=1.55e-6,
    ...     n_eff=2.4,
    ...     radius=10e-6,
    ... )
    >>> print(fsr_l)
    """

    c = 299792458  # speed of light (m/s)

    L = 2 * np.pi * radius

    if use_group_index and dn_eff_dlambda is not None:
        n_g = n_eff - wavelength * dn_eff_dlambda
    else:
        n_g = n_eff

    fsr_lambda = (wavelength**2) / (n_g * L)
    fsr_freq = c / (n_g * L)

    return fsr_lambda, fsr_freq