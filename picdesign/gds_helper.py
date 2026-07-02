from pathlib import Path
from datetime import datetime
import json
import gdsfactory as gf


def export_gds(
    component: gf.Component,
    filename: str | None = None,
    output_dir: str = "gds",
    add_timestamp: bool = False,
    save_metadata: bool = True,
    overwrite: bool = True,
) -> Path:
    """
    Description
    -----------
    Export a gdsfactory component to a GDSII file and optionally
    generate a JSON metadata report. The function automatically
    creates the output directory if it does not exist and can
    append a timestamp to the file name.

    Inputs
    ------
    component : gf.Component
        Photonic component to export.

    filename : str, optional
        Name of the output file without extension.
        If None, the component name is used.

    output_dir : str, optional
        Directory where the GDS file will be saved.

    add_timestamp : bool, optional
        If True, appends the current date and time to the filename.

    save_metadata : bool, optional
        If True, exports a JSON file containing basic component
        information.

    overwrite : bool, optional
        If False, raises an exception when the file already exists.

    Outputs
    -------
    gds_path : pathlib.Path
        Full path to the exported GDS file.

    Units
    -----
    component geometry : µm
        All dimensions inside the component are assumed to follow
        the active PDK units (typically micrometers).

    output_dir : N/A
    filename   : N/A

    Example
    -------
    >>> mzi = gf.components.mzi()
    >>> path = export_gds(
    ...     component=mzi,
    ...     filename="my_mzi",
    ...     output_dir="layout",
    ...     add_timestamp=True,
    ... )
    >>> print(path)
    layout/my_mzi_20260623_103015.gds
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = component.name

    if add_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}"

    gds_path = output_dir / f"{filename}.gds"

    if gds_path.exists() and not overwrite:
        raise FileExistsError(f"{gds_path} already exists.")

    component.write_gds(gds_path)

    if save_metadata:

        metadata = {
            "name": component.name,
            "ports": list(component.ports.keys()),
            "references": len(component.references),
            "timestamp": datetime.now().isoformat(),
        }

        metadata_path = output_dir / f"{filename}.json"

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

    return gds_path