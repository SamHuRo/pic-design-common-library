import numpy as np


def is_single_mode(
    wavelength: float,
    n_core: float,
    n_clad: float,
    width: float,
    height: float,
):
    """
    Description
    -----------
    Approximate single-mode condition check for a rectangular
    integrated photonic waveguide using V-number criteria.

    Inputs
    ------
    wavelength : float
        Operating wavelength (m)

    n_core : float
        Core refractive index

    n_clad : float
        Cladding refractive index

    width : float
        Waveguide width (m)

    height : float
        Waveguide height (m)

    Outputs
    -------
    is_single_mode : bool
        True if approximately single-mode.

    Vx, Vy : float
        Normalized frequency values in x and y directions.

    Units
    -----
    All dimensions in meters.

    Example
    -------
    >>> sm, Vx, Vy = is_single_mode(
    ...     1.55e-6, 2.4, 1.44, 500e-9, 220e-9
    ... )
    """

    k0 = 2 * np.pi / wavelength
    delta_n = np.sqrt(n_core**2 - n_clad**2)

    Vx = k0 * (width / 2) * delta_n
    Vy = k0 * (height / 2) * delta_n

    single_mode = (Vx < np.pi) and (Vy < np.pi)

    return single_mode, Vx, Vy