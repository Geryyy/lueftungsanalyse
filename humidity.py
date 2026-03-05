import numpy as np


def absolute_humidity(temp_c, rel_humidity):
    """Berechnet absolute Feuchte in g/m³.

    AH = 6.112 * exp((17.67 * T) / (T + 243.5)) * RH * 2.1674 / (273.15 + T)

    temp_c        : Temperatur in °C (skalar oder array)
    rel_humidity  : relative Feuchte in % (skalar oder array)
    """
    return (
        6.112
        * np.exp((17.67 * temp_c) / (temp_c + 243.5))
        * rel_humidity
        * 2.1674
        / (273.15 + temp_c)
    )


def cellar_absolute_humidity(temp=None, rh=None):
    """Absolute Feuchte des Kellers anhand von config.py-Werten."""
    import config

    t = temp if temp is not None else config.CELLAR_TEMP
    r = rh if rh is not None else config.CELLAR_RH
    return absolute_humidity(t, r)
