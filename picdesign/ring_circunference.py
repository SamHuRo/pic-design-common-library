import numpy as np


def ring_geometry(radius: float | None = None, circumference: float | None = None):
    """
    Description
    -----------
    Compute ring radius or circumference for integrated photonic
    ring resonators.

    Inputs
    ------
    radius : float, optional
        Ring radius (m)

    circumference : float, optional
        Ring circumference (m)

    Outputs
    -------
    radius : float
        Ring radius (m)

    circumference : float
        Ring circumference (m)

    Units
    -----
    All inputs/outputs in meters.

    Example
    -------
    >>> R, L = ring_geometry(radius=10e-6)
    >>> print(L)
    """

    if radius is None and circumference is None:
        raise ValueError("Provide either radius or circumference.")

    if radius is not None:
        circumference = 2 * np.pi * radius

    else:
        radius = circumference / (2 * np.pi)

    return radius, circumference