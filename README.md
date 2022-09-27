# geoclustering

> 📍 command-line tool for clustering geolocations.

### Features

 - Uses [DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) or [OPTICS](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html) to perform clustering.
 - Outputs clustering results as `json`, `txt` and `geojson`.
 - Creates a [kepler.gl](https://kepler.gl) visualization of clusters.

### Clustering Method

A cluster is created when a certain number of points (defined with `--size`) each are within a given distance (defined with `--distance`) of at least one other point in the cluster. 


## Install

Install with pip:

```sh
# with kepler.gl visualization support
pip install geoclustering[full]

# only text-based output
pip install geoclustering
```

If the `full` install fails, you might need to install kepler.gl build dependencies:

```sh
# macos
brew install proj gdal
```

## Usage

```
Usage: geoclustering [OPTIONS] FILENAME

  Tool to cluster geolocations. A cluster is created when a certain number of
  points (defined with --size) each are within a given distance (defined with
  --distance) of at least one other point in the cluster. Input is supplied as
  a csv file. At a minimum, each row needs to have a 'lat' and a 'lon' column.
  Other rows are reflected to the output.

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
  --open                          Open the generated visualization in the
                                  default browser automatically.
  --debug                         Print debug output.
  --help                          Show this message and exit.
```

## Input

Inputs are supplied as a `.csv` file. At a minimum, each row needs to have a `lat` and a `lon`` column. Other rows are reflected to the output.

```csv
id,name,lat,lon
1,Bonnibelle Mathwen,40.1324085,64.4911086
...
```

## Output

If at least one cluster was found, the tool outputs a folder with output as `json`, `geojson`, `txt`, `csv` files. A kepler.gl `html` file is generated as well.

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

### Text

Encodes cluster as blocks separated by a newline, where each line in a cluster block contains one point.

```txt
Cluster 0
id 9, name Rosanna Foggo, lat -6.2074293, lon 106.8915948

// ...
```

### CSV

Encodes each event in one line with `cluster_id` information associated.

```csv
cluster_id,name,lat,lon
9,Rosanna Foggo,-6.2074293,106.8915948
...
```

### kepler.gl

![kepler.gl instance](https://user-images.githubusercontent.com/1682504/176478177-c0446b51-4060-495c-803d-79e2bbd3e966.png)

## Develop

It is assumed that you are using **Python3.9+**. It is encouraged to [setup a virtualenv](https://wiki.archlinux.org/title/Python/Virtual_environment#venv>) for development.

```sh
    # install dependencies & dev-dependencies
    # PIP
    pip install -e .[dev,full]
    # PIPENV
    pipenv install --dev -e .

    # install a git hook that runs the code formatter before each commit.
    pre-commit install
```

We use [Black](https://github.com/psf/black) as our code formatter. If you don't want to use the `pre-commit` hook, you can run the formatter manually or via an editor plugin.
