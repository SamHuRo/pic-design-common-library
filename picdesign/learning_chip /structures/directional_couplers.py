from wcwidth import width

import gdsfactory as gf

def directional_coupler_SiN_1550(
        params: dict
) -> gf.Component:
    """Returns a directional coupler component.

    Args:
        params: A dictionary containing the parameters for the directional coupler.
            Expected keys:
                - 'chip_height': Height of the chip (float).
                - 'chip_width': Width of the chip (float).
                - 'margin': Margin around the chip (float).
                - 'length': Length of the waveguides (float).
                - 'width': Width of the waveguides (float).
                - 'ratio_coupling': Coupling ratio (str).
                - 'gap': Gap between the two waveguides (float).

    Returns:
        A gdsfactory Component representing the directional coupler.
    """
    # =============================================================
    #        Extract parameters from the input dictionary
    # =============================================================
    chip_height = params['chip_height']
    chip_width = params['chip_width']
    margin = params['margin']
    length = params['length']
    width = params['width']
    ratio_coupling = params['ratio_coupling']
    gap = params['gap']
    type_bend = params['type_bend']
    dy_coupler_value = params['dy_coupler_value']
    dx_coupler_value = params['dx_coupler_value']

    # =============================================================
    #      Create the directional coupler component
    # =============================================================
    c = gf.Component(
        name="directional_coupler"
    )

    # Definition of the usable area for the directional coupler
    usable_height = chip_height - 2 * margin
    usable_width = chip_width - 2 * margin

    # Definition 
    a_por_ratio = {
        "50:50": 4,
        "0:100": 2,
        "25:75": 7/36,
    }

    for idx, (ratio_coupler_value, gap_coupler_value) in enumerate(zip(ratio_coupling, gap)):
        # Reference structure
        structure = gf.Component()

        a = a_por_ratio[ratio_coupler_value]

        # Definition of the directional coupler
        dc_component = structure.add_ref(
            gf.components.directional_coupler(
                gap=gap_coupler_value, 
                length=length, 
                dy=dy_coupler_value,
                dx=dx_coupler_value,
                cross_section=gf.cross_section.strip(
                    width=width, 
                    layer=(1, 0),
                    port_names=("o1", "o2")
                ),
                allow_min_radius_violation=False,
                bend=type_bend
            )
        )
        

    # Create the two waveguides
    wg1 = gf.components.straight(length=length, width=width)
    wg2 = gf.components.straight(length=length, width=width)

    # Position the second waveguide with the specified gap
    wg2_ref = wg2.ref()
    wg2_ref.move((0, width + gap))

    # Create a new component and add both waveguides
    coupler = gf.Component("directional_coupler")
    coupler.add(wg1)
    coupler.add(wg2_ref)

    return coupler