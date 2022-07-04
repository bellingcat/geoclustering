from geoclustering.clustering import cluster_locations
from geoclustering.encoding import encode_clusters
from tests.helpers import read_fixture_csv, read_fixture_content


df = read_fixture_csv("clustering.csv")


def test_encoders():
    clusters = {
        0: [
            {"id": 1, "name": "Alice", "lat": 52.523955, "lon": 13.442362},
            {"id": 2, "name": "Bob", "lat": 52.526659, "lon": 13.448097},
        ],
        1: [
            {"id": 3, "name": "Carol", "lat": 52.525626, "lon": 13.419246},
            {
                "id": 4,
                "name": "Dan",
                "lat": 52.52443559865125,
                "lon": 13.41261723049818,
            },
        ],
    }

    res = encode_clusters(clusters)

    assert res["string"] == read_fixture_content("snapshots/result.txt")
    assert res["json"] == read_fixture_content("snapshots/result.json")
    assert res["geojson"] == read_fixture_content("snapshots/result.geojson")
