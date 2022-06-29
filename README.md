# geocluster

> 📍 command-line tool for clustering geolocations.

### Features

 - Uses [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) or [OPTICS](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html) to perform clustering.
 - Outputs clustering results as `json`, `txt` and `geojson`.
 - Creates a [kepler.gl](https://kepler.gl) visualization of clusters.

### Clustering Method

A cluster is created when a certain number of points (=> `--size`) each are within a given distance (=> `--distance`) of at least one other point in the cluster. 


## Install

Clone the repository:

```sh
git clone https://github.com/fspoettel/geocluster
cd geocluster
```

Install keplergl build dependencies:

```sh
# macos
brew install proj gdal
```

Install project with pip:
```sh
pip install .
```

## Usage

```
Usage: geocluster [OPTIONS] FILENAME

Options:
  -d, --distance FLOAT            (in km) Max. distance between two points in
                                  a cluster.  [required]
  -s, --size INTEGER              Min. number of points in a cluster.
                                  [required]
  -o, --output PATH               Output directory for results. Default:
                                  ./output
  -a, --algorithm [dbscan|optics]
                                  Clustering algorithm to be used. `optics`
                                  produces tighter clusters but is slower.
                                  Default: dbscan
  --help                          Show this message and exit.
```

## Input

Inputs are supplied as a `.csv` file. The only required fields are `lat` and `lon`, all other fields are reflected to the output.

```csv
id,name,lat,lon
1,Bonnibelle Mathwen,40.1324085,64.4911086
...
```

## Output

If at least one cluster was found, the tool outputs a folder with `json`, `geojson`, `text` and a kepler.gl `html` files.

### JSON

Encodes an array of clusters, each containing an array of points.

```json
[
  {
    "cluster_id": 0,
    "points": [
      {
        "id": 9,
        "name": "Rosanna Foggo",
        "lat": -6.2074293,
        "lon": 106.8915948
      }
    ]
  }
]
```

### GeoJSON

Encodes a single `FeatureCollection`, containing all points as `Feature` objects.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          106.891595,
          -6.207429
        ]
      },
      "properties": {
        "id": 9,
        "name": "Rosanna Foggo",
        "cluster_id": 0
      }
    }
  ]
}
```

### txt

Encodes cluster as blocks separated by a newline, where each line in a cluster block contains one point.

```txt
Cluster 0
id 9, name Rosanna Foggo, lat -6.2074293, lon 106.8915948

// ...
```

### kepler.gl

![kepler.gl instance](https://user-images.githubusercontent.com/1682504/176478177-c0446b51-4060-495c-803d-79e2bbd3e966.png)
