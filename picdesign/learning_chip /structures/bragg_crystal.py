import gdsfactory as gf

def bragg_crystal_SiN(
        params: dict
) -> gf.Component:
    """Returns a Bragg crystal component.

    Args:
        params: A dictionary containing the parameters for the Bragg crystal.
            Expected keys:
                - 'chip_height': Height of the chip (float).
                - 'chip_width': Width of the chip (float).
                - 'margin': Margin around the chip (float).
                - 'length': Total length of the spiral (float).
                - 'width': Width of the waveguides (float).
                - 'type_bend': Type of bend for the waveguides (str).
                - 'dy_coupler_value': Vertical offset for the coupler (float).
                - 'dx_coupler_value': Horizontal offset for the coupler (float).
                - 'type_spiral': Type of spiral to create ['s', 'race_track'] (str).
                - 'type_coupler': Type of coupler to use ['edge_coupler', 'grating_coupler'] (str).
                - 'length_tapper': Length of the taper section (float).
                - 'dx_spiral': Horizontal offset for the spiral (float).
                - 'dy_spiral': Vertical offset for the spiral (float).

    Returns:
        A gdsfactory Component representing the spiral.
    """

    # =============================================================
    #       Extract parameters from the input dictionary
    # =============================================================


    # =============================================================
    #      Create the Bragg crystal component
    # =============================================================
    c = gf.Component()

    return c