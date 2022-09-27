import json
import numpy as np
import geojson
import csv
import io  # not io.py


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


class CSVEncoder:
    """Encodes clustering result as a CSV"""

    def __init__(self):
        self.state = io.StringIO()
        self.writer = False

    def visitor(self, cluster_id, cluster):
        if not self.writer:
            self.writer = csv.DictWriter(
                self.state,
                fieldnames=["cluster_id"] + list(cluster[0].keys()),
                quoting=csv.QUOTE_NONNUMERIC,
            )
            self.writer.writeheader()

        for record in cluster:
            self.writer.writerow({**record, "cluster_id": cluster_id})

    def get(self):
        return self.state.getvalue()


def encode_clusters(clusters):
    json_encoder = JSONEncoder()
    geojson_encoder = GeoJSONEncoder()
    string_encoder = StringEncoder()
    csv_encoder = CSVEncoder()

    encoders = [json_encoder, geojson_encoder, string_encoder, csv_encoder]
    for cluster_id, cluster in clusters.items():
        for encoder in encoders:
            encoder.visitor(cluster_id, cluster)

    return {
        "json": json_encoder.get(),
        "geojson": geojson_encoder.get(),
        "string": string_encoder.get(),
        "csv": csv_encoder.get(),
    }
