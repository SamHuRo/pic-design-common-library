import numpy as np


def dbcm_to_inv_m(alpha_db_cm: float) -> float:
    """
    Convert propagation loss from dB/cm to m^-1 (Neper/m).
    """
    return (np.log(10) / 10) * 100 * alpha_db_cm


def invm_to_dbcm(alpha_m_inv: float) -> float:
    """
    Convert propagation loss from m^-1 (Neper/m) to dB/cm.
    """
    return (10 / np.log(10)) * (alpha_m_inv / 100)