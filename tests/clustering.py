import os
from geocluster.clustering import cluster_locations
from geocluster.io import read_csv_file


def get_fixture_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, "fixtures/clustering.csv")


def has_member(list, name):
    return any(x for x in list if x["name"] == name)


def test_clustering_all():
    df = read_csv_file(get_fixture_path())
    # there should be one cluster with all members but Erin.
    res = cluster_locations(
        df=df, algorithm="dbscan", radius_km=1.97, min_cluster_size=4
    )
    assert len(res.values()) == 1
    assert len(res[0]) == 4


def test_clustering_split():
    df = read_csv_file(get_fixture_path())
    res = cluster_locations(
        df=df, algorithm="dbscan", radius_km=0.5, min_cluster_size=2
    )
    # there should be two cluster: Alice & Bob and Carol & Dan
    assert len(res.values()) == 2
    cluster_one = res[0]
    cluster_two = res[1]
    assert len(cluster_one) == 2
    assert has_member(cluster_one, "Alice")
    assert has_member(cluster_one, "Bob")
    assert has_member(cluster_two, "Carol")
    assert has_member(cluster_two, "Dan")


def test_clustering_none():
    df = read_csv_file(get_fixture_path())
    # there should be no clusters now.
    res = cluster_locations(
        df=df, algorithm="dbscan", radius_km=0.5, min_cluster_size=3
    )
    assert len(res.values()) == 0
