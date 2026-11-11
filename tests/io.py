from pathlib import Path
import shutil
import pytest
from geoclustering.io import read_csv_file, write_output_file
from tests.helpers import read_fixture_csv


def test_csv_filters():
    df = read_fixture_csv("io.csv")
    # entries 2 & 5 in fixture are valid.
    assert len(df) == 2
    assert df.iloc[0]["name"] is None
    assert df.iloc[1]["name"] == "Bob"


def test_csv_without_lat_lon_columns_raises_clean_error(tmp_path):
    csv_path = tmp_path / "nocoords.csv"
    csv_path.write_text("name,city\nAlice,Paris\nBob,London\n")

    with pytest.raises(ValueError, match="'lat' and 'lon'"):
        read_csv_file(str(csv_path))


def test_write_output_file():
    p = "./this/dir/does/not/exist"
    f = "test.txt"
    write_output_file(p, f, "test")

    path = Path(p) / f

    with open(path) as f:
        assert f.read() == "test"

    shutil.rmtree(Path("./this"))
