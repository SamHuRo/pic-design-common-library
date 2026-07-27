import gdsfactory as gf

def ring_SiN_1550(
        params: dict
) -> gf.Component:
    """Returns a ring resonator component.

    Args:
        params: A dictionary containing the parameters for the ring resonator.
            Expected keys:
                - 'chip_height': Height of the chip (float).
                - 'chip_width': Width of the chip (float).
                - 'margin': Margin around the chip (float).
                - 'length': Total length of the spiral (float).
                - 'width': Width of the waveguides (float).
                - 'type_bend': Type of bend for the waveguides (str).
                - 'dy_coupler_value': Vertical offset for the coupler (float).
                - 'dx_coupler_value': Horizontal offset for the coupler (float).
                - 'type_spiral': Type of spiral to create ['s', 'race_track']

    """
    # =============================================================
    #       Extract parameters from the input dictionary
    # =============================================================
    gap = params['gap']
    wg_width = params['wg_width']
    radius = params['ring_radius']
    angle_resolution = params['angle_resolution']
    angle = params['angle']
    wg_length = params['wg_length']
    taper_length = params['taper_length']
    grating_coupler = params['grating_coupler']
    fsr = params['FSR']

    # =============================================================
    #      Create the ring resonator component
    # =============================================================
    c = gf.Component()

    structure = gf.Component()

    # =============================================================
    #     Create the ring resonator structure
    # =============================================================
    # Structure of the ring resonator
    structure.add_ref(
            gf.components.ring(
            radius=radius, 
            width=wg_width, 
            angle_resolution=angle_resolution, 
            layer='WG', 
            angle=angle
        ).copy()
    )

    if grating_coupler:
        wg_straight = structure.add_ref(
            gf.components.straight(
                length=wg_length,
                cross_section=gf.cross_section.strip(width=wg_width, layer='WG')
            )
        ).move((- wg_length / 2, -(radius + gap + wg_width)))

        # Creating the taper for the input of the grating coupler
        taper_in = structure.add_ref(
            gf.components.taper(
                length= taper_length,
                width1= 0.5,
                width2= wg_width,
                cross_section= gf.cross_section.strip
            )
        )
        taper_in.connect(taper_in.ports["o2"], wg_straight.ports["o1"])

        # Creating the grating couplers for the input of the structure
        gc_in = structure.add_ref(
            gf.components.grating_couplers.grating_coupler_elliptical(
                polarization='te', 
                taper_length=16.6, 
                taper_angle=40.0, 
                wavelength=1.55, 
                fiber_angle=15.0, 
                grating_line_width=0.343, 
                neff=n_eff, 
                nclad=1.443, 
                n_periods=30, 
                big_last_tooth=False, 
                layer_slab='SLAB150', 
                slab_xmin=-1.0, 
                slab_offset=2.0, 
                spiked=True, 
                cross_section='strip'
            )
        )
        gc_in.connect(gc_in.ports["o1"], taper_in.ports["o1"])

        # Creating the taper for the input of the grating coupler
        taper_out = structure.add_ref(
            gf.components.taper(
                length= taper_length,
                width1= wg_width,
                width2= 0.5,
                cross_section= gf.cross_section.strip
            )
        )
        taper_out.connect(taper_out.ports["o1"], wg_straight.ports["o2"])

        # Creating the grating couplers for the output of the structure
        gc_out = structure.add_ref(
            gf.components.grating_couplers.grating_coupler_elliptical(
                polarization='te', 
                taper_length=16.6, 
                taper_angle=40.0, 
                wavelength=1.55, 
                fiber_angle=15.0, 
                grating_line_width=0.343, 
                neff=n_eff, 
                nclad=1.443, 
                n_periods=30, 
                big_last_tooth=False, 
                layer_slab='SLAB150', 
                slab_xmin=-1.0, 
                slab_offset=2.0, 
                spiked=True, 
                cross_section='strip'
            )
        )
        gc_out.connect(gc_out.ports["o1"], taper_out.ports["o2"])
    else:
        wg_straight = structure.add_ref(
            gf.components.straight(
                length=4000,
                cross_section=gf.cross_section.strip(width=wg_width, layer='WG')
            )
        ).move((- 4000 / 2, -(radius + gap + wg_width) ))

        # Creating the taper for the input of the grating coupler
        taper_in = structure.add_ref(
            gf.components.taper(
                length= 500,
                width1= 0.5,
                width2= wg_width,
                cross_section= gf.cross_section.strip
            )
        )
        taper_in.connect(taper_in.ports["o2"], wg_straight.ports["o1"])
        taper_in.move((- 500, 0))

        # Creating the taper for the input of the grating coupler
        taper_out = structure.add_ref(
            gf.components.taper(
                length= 500,
                width1= wg_width,
                width2= 0.5,
                cross_section= gf.cross_section.strip
            )
        )
        taper_out.connect(taper_out.ports["o1"], wg_straight.ports["o2"])

    # Labeling the structure
    structure.add_ref(
        gf.components.text(
            text= f"Ring: FSR {fsr} with R : {radius:.1f} - Gap {gap} um",
            size= 50,
            position=(wg_length + 100, radius + gap + wg_width + 10),
            justify= "left",
            layer= "WG"
        )
    )

    c.add_ref(structure)

    return c