from pathlib import Path
from geocluster.io import write_output_file
from tests.helpers import read_fixture_csv


def test_csv_filters():
    df = read_fixture_csv("io.csv")
    # entries 2 & 5 in fixture are valid.
    assert len(df) == 2
    assert df.iloc[0]["name"] == None
    assert df.iloc[1]["name"] == "Bob"


def test_write_output_file():
    p = "./this/dir/does/not/exist"
    f = "test.txt"
    write_output_file(p, f, "test")

    path = Path(p) / f

    with open(path) as f:
        assert f.read() == "test"

    path.unlink()
