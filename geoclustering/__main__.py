from pathlib import Path
import click
import os
import webbrowser

import geoclustering.clustering as clustering
import geoclustering.encoding as encoding
import geoclustering.io as io


def print_debug(s):
    click.secho(s, fg="bright_black")


@click.command(
    help="Tool to cluster geolocations. A cluster is created when a certain number of points (--size) each are within a given distance (--distance) of at least one other point in the cluster. Input is supplied as a csv file. At a minimum, each row needs to have a 'lat' and a 'lon' column. Other rows are reflected to the output."
)
@click.option(
    "--distance",
    "-d",
    type=click.FLOAT,
    required=True,
    help="(in km) Max. distance between two points in a cluster.",
)
@click.option(
    "--size",
    "-s",
    type=click.INT,
    required=True,
    help="Min. number of points in a cluster.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=False),
    default="output",
    help="Output directory for results. Default: ./output",
)
@click.option(
    "--algorithm",
    "-a",
    type=click.Choice(
        ["dbscan", "optics"],
        case_sensitive=False,
    ),
    default="dbscan",
    help="Clustering algorithm to be used. `optics` produces tighter clusters but is slower. Default: dbscan",
)
@click.option(
    "--open",
    is_flag=True,
    help="Open the generated visualization in the default browser automatically.",
)
@click.option("--debug", is_flag=True, help="Print debug output.")
@click.argument("filename", type=click.Path(exists=True))
def main(distance, size, output, filename, algorithm, open, debug):
    if debug:
        print_debug(f"Reading input from {Path(filename).absolute()}")

    df = io.read_csv_file(filename)
    if debug:
        print_debug(f"Read {len(df)} valid coordinates")

    clusters = clustering.cluster_locations(
        df=df, algorithm=algorithm, radius_km=distance, min_cluster_size=size
    )

    if not bool(clusters):
        click.echo("Did not find clusters matching input parameters.")
        return

    print_debug(f"Found {len(clusters)} valid clusters using {algorithm}")

    encoded = encoding.encode_clusters(clusters)

    io.write_output_file(output, "result.txt", encoded["string"])
    io.write_output_file(output, "result.json", encoded["json"])
    io.write_output_file(output, "result.geojson", encoded["geojson"])
    vis = io.write_visualization(output, "result.html", encoded["geojson"])
    click.echo(f"Output files saved to {Path(output).absolute()}")

    if open:
        print_debug(f"Opening visualization in default browser")
        webbrowser.open_new_tab("file://" + str(vis.absolute()))


if __name__ == "__main__":
    main()
