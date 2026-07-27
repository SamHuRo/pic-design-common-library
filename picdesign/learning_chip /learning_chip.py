import gdsfactory as gf
from datetime import date
from structures import spirals, rings, bragg_crystal
from gdsfactory.generic_tech import get_generic_pdk

# Activate PDK
get_generic_pdk().activate()

now = date.today()

name_chip = f"learning_chip_{now.strftime('%d-%m-%Y')}"

# Creation of the learning chip 
learning_chip = gf.Component(name_chip)

chip_width = 4330 # 4.33 mm ->  um
chip_height = 2000 # um

# ===================================================
#           Add the spirals to the learning chip
# ===================================================
# A cm of diference between the length of the spirals is used to avoid overlapping of the structures in the learning chip.
list_of_lengths = [1000, 2000, 3000, 4000, 5000, 6000]

# List for the separation of the spirals in the learning chip
dx = 800

# List of widths for the spirals in the learning chip
list_of_widths = [1, 0.6, 0.4]

spiral_refs = []
spacing_between_spirals = 40
free_top_edge = None

for j, width in enumerate(list_of_widths):
    for i, length in enumerate(list_of_lengths):
        params_spirals = {
            'chip_width': chip_width,
            'margin': 0,
            'length': length,
            'width_singlemode': width,
            'width_tapper': 10,
            'num_bends': 4,
            'type_bend': 'circular',
            'dy_coupler_value': 0.5,
            'dx_coupler_value': 0.5,
            'wavelength': 1.55,
            'type_spiral': 's',
            'type_coupler': 'edge_coupler',
            'length_tapper': 200,
            'dx_spiral': dx * (-1)**(i + 1),
            'dy_spiral': 0,
            'bend_radius': 30,
        }

        spiral = spirals.spiral_SiN_1550(
            params=params_spirals
        )

        # The total y length of the spiral
        spiral_y_size = spiral.ysize
        print(f"The total y size of the spiral is: {spiral_y_size} um")

        # Local position (before moving) of the input waveguide
        in_port_y_local = spiral.ports["in_wg"].center[1]
        print(f"Local position of the spiral: {in_port_y_local}")

        # How far does the spiral extend below and above its own entry guide
        bottom_extent = in_port_y_local - spiral.ymin
        print(f"Spiral extend: {bottom_extent}")
        top_extent = spiral.ymax - in_port_y_local
        print(f"Top of the spiral: {top_extent}")

        if i % 2 != 0:
            # The entry guide for this spiral is located “spacing_between_spirals”
            # above the occupied top edge, leaving room for bottom_extent
            target_in_port_y = free_top_edge + spacing_between_spirals + bottom_extent
            print(f"Position of the y port: {target_in_port_y}")
            dy = target_in_port_y - spiral_y_size
            print(f"Mismatch in the y axis: {dy}")
        else:
            if free_top_edge is None:
                dy = -in_port_y_local
                print(f"Mismatch in the y axis: {dy}")
            else:
                target_in_port_y = free_top_edge + spacing_between_spirals + bottom_extent
                print(f"Position of the y port: {target_in_port_y}")
                dy = free_top_edge + spiral_y_size + spacing_between_spirals
                print(f"Mismatch in the y axis: {dy}")

        spiral_ref = learning_chip << spiral
        spiral_ref.move((0, dy))
        spiral_refs.append(spiral_ref)

        # Update the occupied top margin based on the final position
        free_top_edge = spiral_ref.ymax
        print(f"Top margin update: {free_top_edge}")
        print(20 * "=")

    text_label = gf.components.text(
        text=f"Spiral width: {width} um",
        size=50,
        position=(-chip_width / 2 + 550, free_top_edge + 50),
        justify="center",
        layer="WG"
    )
    learning_chip.add_ref(text_label)

    # Update the occupied top margin based on the final position
    # free_top_edge += text_label.ysize + 50


# ==========================================================
#    Add the rings to the learning chip
# ==========================================================
params_rings = {
    'chip_height': chip_height,
    'chip_width': chip_width,
    'margin': 0,
    'gap': 0.2,
}


# ==========================================================
#      See the final structure of the learning chip
# ==========================================================
learning_chip.ports
learning_chip.draw_ports()
learning_chip.pprint_ports()
learning_chip.plot()

# Write out the final GDS file
gds_filename = name_chip + ".gds"
learning_chip.write_gds(gds_filename)
learning_chip.show()




