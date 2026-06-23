import numpy as np


def mzi_path_imbalance(
    L1: float,
    L2: float,
    wavelength: float,
    n_eff: float,
    n_group: float | None = None,
):
    """
    Description
    -----------
    Compute path-length imbalance and key optical properties
    of a Mach-Zehnder Interferometer (MZI).

    Inputs
    ------
    L1 : float
        Length of arm 1 (m)

    L2 : float
        Length of arm 2 (m)

    wavelength : float
        Operating wavelength (m)

    n_eff : float
        Effective refractive index

    n_group : float, optional
        Group index. If None, n_eff is used as approximation.

    Outputs
    -------
    delta_L : float
        Path-length imbalance (m)

    delta_phi : float
        Phase difference (rad)

    fsr_lambda : float
        Approximate free spectral range (m)

    Units
    -----
    All lengths in meters.

    Example
    -------
    >>> dL, phi, fsr = mzi_path_imbalance(
    ...     100e-6, 120e-6, 1.55e-6, 2.4
    ... )
    """

    c = 299792458

    if n_group is None:
        n_group = n_eff

    delta_L = L2 - L1

    delta_phi = (2 * np.pi / wavelength) * n_eff * delta_L

    fsr_lambda = (wavelength**2) / (n_group * delta_L) if delta_L != 0 else np.inf

    return delta_L, delta_phi, fsr_lambda