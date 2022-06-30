import json
import numpy as np
import geojson


class NpEncoder(json.JSONEncoder):
    """JSONEncoder with support for numpy's numerical types."""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super(NpEncoder, self).default(obj)


class StringEncoder:
    """Encodes clustering result as a string."""

    def __init__(self):
        self.state = []

    def visitor(self, cluster_id, cluster):
        self.state.append("Cluster {}".format(cluster_id))

        for record in cluster:
            s = []
            for key, val in record.items():
                s.append("{} {}".format(key, val))
            self.state.append(", ".join(s))

        # separate clusters by an empty line.
        self.state.append("")

    def get(self):
        return "\n".join(self.state)


class JSONEncoder:
    """Encodes clustering result as a JSON array."""

    def __init__(self):
        self.state = []

    def visitor(self, cluster_id, cluster):
        cluster_data = {"cluster_id": cluster_id, "points": []}

        for record in cluster:
            cluster_data["points"].append(record)
            self.state.append(cluster_data)

    def get(self):
        return json.dumps(self.state, cls=NpEncoder)


class GeoJSONEncoder:
    def __init__(self):
        self.state = []

    def visitor(self, cluster_id, cluster):
        for record in cluster:
            props = {
                **record,
                "cluster_id": cluster_id,
            }

            lon = float(props.pop("lon"))
            lat = float(props.pop("lat"))

            point = geojson.Point((lon, lat))
            self.state.append(geojson.Feature(geometry=point, properties=props))

    def get(self):
        return json.dumps(geojson.FeatureCollection(self.state), cls=NpEncoder)


def encode_clusters(clusters):
    json_encoder = JSONEncoder()
    geojson_encoder = GeoJSONEncoder()
    string_encoder = StringEncoder()

    encoders = [json_encoder, geojson_encoder, string_encoder]

    for cluster_id, cluster in clusters.items():
        for encoder in encoders:
            encoder.visitor(cluster_id, cluster)

    return {
        "json": json_encoder.get(),
        "geojson": geojson_encoder.get(),
        "string": string_encoder.get(),
    }
