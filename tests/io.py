from tests.helpers import read_fixture_csv


def test_csv_filters():
    df = read_fixture_csv("io.csv")
    # entries 2 & 5 in fixture are valid.
    assert len(df) == 2
    assert df.iloc[0]["name"] == None
    assert df.iloc[1]["name"] == "Bob"
