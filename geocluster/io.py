from keplergl import KeplerGl
from pathlib import Path
from pkg_resources import resource_filename
import json
import json
import pandas as pd


def read_csv_file(filename):
    """Read input csv file, dropping rows that don't have valid location data."""
    return pd.read_csv(filename).dropna(subset=["lat", "lon"])


def ensure_file_path(dirname, filename):
    """Ensure a parent directory exists for a file."""
    path = Path(dirname)
    path.mkdir(parents=True, exist_ok=True)
    return path / filename


def write_output_file(dirname, filename, data):
    """Write a file, ensuring parent directories."""
    filepath = ensure_file_path(dirname, filename)

    with open(filepath, "w") as f:
        f.write(data)

    return filepath


def write_visualization(dirname, filename, data):
    """Write a visualization, ensuring parent directories."""
    map = KeplerGl()
    map.add_data(data=data, name="clusters")

    # config configures a default color scheme for our clusters layer.
    config_file = resource_filename("geocluster", "kepler_config.json")
    with open(config_file) as f:
        map.config = json.loads(f.read())

    filepath = ensure_file_path(dirname, filename)
    map.save_to_html(file_name=str(filepath), center_map=True)

    return filepath
