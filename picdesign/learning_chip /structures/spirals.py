import gdsfactory as gf


def _get_racetrack(length, cross_section, max_tries=10):
    n = 8
    for _ in range(max_tries):
        try:
            return gf.components.spiral_racetrack_fixed_length(
                length=length,
                in_out_port_spacing=150,
                n_straight_sections=n,
                min_spacing=5,
                bend='bend_circular',
                bend_s='bend_s',
                cross_section=cross_section,
            )
        except ValueError:
            n += 4  # incrementa hasta que quepa
    raise ValueError(f"No se pudo generar spiral de {length} µm tras {max_tries} intentos.")

# ================================================================================
#           Function to create the spiral component for the plataform of SiN,
#           with a center wavelength of 1550 nm.
# ================================================================================
def spiral_SiN_1550(
        params: dict
) -> gf.Component:
    """Returns a spiral component.

    Args:
        params: A dictionary containing the parameters for the spiral.
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
    #        Extract parameters from the input dictionary
    # =============================================================
    chip_width = params['chip_width']
    margin = params['margin']
    length = params['length']
    width_singlemode = params['width_singlemode']
    width_tapper = params['width_tapper']
    num_bends = params['num_bends']
    length_tapper = params['length_tapper']
    type_spiral = params['type_spiral']
    type_bend = params['type_bend']
    type_coupler = params['type_coupler']
    dy_coupler_value = params['dy_coupler_value']
    dx_coupler_value = params['dx_coupler_value']
    dx_spiral = params['dx_spiral']
    bend_radius = params['bend_radius']  # Default bend radius if not provided

    # =============================================================
    #      Create the spiral component
    # =============================================================
    c = gf.Component()

    structure = gf.Component()

    # Definition of the usable area for the directional coupler
    usable_width = chip_width - 2 * margin

    # Definition of the cross section of the waveguide
    cross_section_singlemode = gf.cross_section.strip(
            width=width_singlemode, 
            layer=(1, 0),
            port_names=("o1", "o2")
    )

    # List of types of spirals
    spiral_types = {
        's': gf.components.delay_snake2(
                length=length, 
                length0=0, 
                length2=0, 
                n=num_bends, 
                bend180={
                    "component": "bend_euler180",
                    "settings": {"radius": bend_radius}  # ajusta el valor en µm que necesites
                }, 
                cross_section= cross_section_singlemode,
        ), 
        # 'race_track': _get_racetrack(length, cross_section_singlemode),
    }

    # ==================================================================================
    #    Create the spiral structures based on the specified parameters
    # ==================================================================================
    # Creation of the spiral using gdsfactory
    spiral = spiral_types[type_spiral]

    # Add the spiral to the reference component
    spiral_ref = structure.add_ref(spiral)

    # Position of the ports of the spiral structure
    p1_spiral = spiral_ref.ports["o1"].center
    p2_spiral = spiral_ref.ports["o2"].center

    # Calculation of the delta length for the spiral
    delta_length = p2_spiral[0] - p1_spiral[0]
    print(f"Delta length for the spiral: {delta_length} µm")

    # Move the spiral to the center of the usable area of the chip
    spiral_ref.move((- delta_length / 2, 0))

    # Move the spiral to a position defined by the user in the parameters dictionary
    spiral_ref.move((dx_spiral, 0))

    # Error to detect if the delta length exceeds the usable width of the chip
    if delta_length > usable_width:
        raise ValueError(f"Delta length {delta_length} µm exceeds usable width {usable_width} µm.")

    # ==================================================================================
    #               Definition of the waveguides to de edge or grating couplers
    # ==================================================================================
    wg_spiral_length = 250

    # Waveguide input to the spiral
    wg_input_ref = structure.add_ref(
        gf.components.straight(
            length=wg_spiral_length,
            cross_section=cross_section_singlemode
        )
    )   

    # Waveguide output from the spiral
    wg_output_ref = structure.add_ref(
        gf.components.straight(
            length=wg_spiral_length,
            cross_section=cross_section_singlemode
        )
    )

    wg_input_ref.connect("o2", spiral_ref.ports["o1"])
    wg_output_ref.connect("o1", spiral_ref.ports["o2"])

    # ===============================================================================
    #                           Definition of the tapper section
    # ===============================================================================
    tapper = gf.components.taper(
        length=length_tapper,
        width1=width_singlemode,
        width2=width_tapper,
        cross_section=gf.cross_section.strip
    )

    # Tapper input to the spiral
    tapper_input_ref = structure.add_ref(tapper)
    tapper_input_ref.connect("o1", wg_input_ref.ports["o1"])

    # Tapper output from the spiral
    tapper_output_ref = structure.add_ref(tapper)
    tapper_output_ref.connect("o1", wg_output_ref.ports["o2"])

    # =============================================================================================
    #  Add the type of coupler to the spiral structutre, either edge coupler or grating coupler
    # =============================================================================================
    # Base length of each coupler if the spiral were centered (dx_spiral = 0)
    base_coupler_length = usable_width / 2 - delta_length / 2 - length_tapper - wg_spiral_length

    # When the dx_spiral is moved to the right (positive), the input side
    # gains space and the output side loses the same amount, and vice versa.
    length_coupler_input = base_coupler_length + dx_spiral
    length_coupler_output = base_coupler_length - dx_spiral

    coupler_type_input = {
        'edge_coupler': gf.components.straight(
            length=length_coupler_input,
            cross_section=gf.cross_section.strip(
                    width=width_tapper, 
                    layer=(1, 0),
                    port_names=("o1", "o2")
            )
        ),
        # 'grating_coupler': gf.components.grating_coupler_elliptical_te(
        #     wavelength=1.55,
        #     grating_period=0.63,
        #     duty_cycle=0.5,
        #     width=width,
        #     n_periods=20,
        #     layer=(1, 0),
        #     port_names=("o1", "o2")
        # )
    }

    coupler_type_output = {
        'edge_coupler': gf.components.straight(
            length=length_coupler_output,
            cross_section=gf.cross_section.strip(
                    width=width_tapper, 
                    layer=(1, 0),
                    port_names=("o1", "o2")
            )
        ),
        # 'grating_coupler': gf.components.grating_coupler_elliptical_te(
        #     wavelength=1.55,
        #     grating_period=0.63,
        #     duty_cycle=0.5,
        #     width=width,
        #     n_periods=20,
        #     layer=(1, 0),
        #     port_names=("o1", "o2")
        # )
    }

    # Add the selected coupler structure to the spiral component
    coupler_structure_input = coupler_type_input[type_coupler]
    coupler_input_ref = structure.add_ref(coupler_structure_input)
    coupler_input_ref.connect("o2", tapper_input_ref.ports["o2"])

    coupler_structure_output = coupler_type_output[type_coupler]
    coupler_output_ref = structure.add_ref(coupler_structure_output)
    coupler_output_ref.connect("o1", tapper_output_ref.ports["o2"])

    # ================================================================
    # Add the text label to the spiral structure
    # ================================================================
        # Add the text label for the spiral length
    text_label = gf.components.text(
        text=f"{length} um",
        size=55,
        position=(spiral_ref.xmax + 100, p2_spiral[1] + 50),
        justify= "left",
        layer= "WG"
    )
    structure.add_ref(text_label)

    # =================================================================
    #   Add the spiral to the main component
    # =================================================================
    structure.add_port("in_wg", port=coupler_input_ref.ports["o1"])
    structure.add_port("out_wg", port=coupler_output_ref.ports["o2"])

    ref = c.add_ref(structure)
    c.add_ports(ref.ports)

    return c





