from pathlib import Path
import click
import os
import webbrowser

import geoclustering.clustering as clustering
import geoclustering.encoding as encoding
import geoclustering.io as io


@click.command(
    help="Tool to cluster geolocations. A cluster is created when a certain number of points (defined with --size) each are within a given distance (defined with --distance) of at least one other point in the cluster. Input is supplied as a csv file. At a minimum, each row needs to have a 'lat' and a 'lon' column. Other rows are reflected to the output."
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
    def print_debug(s):
        if debug:
            click.secho(s, fg="bright_black")

    df = io.read_csv_file(filename)
    print_debug(f"Read {len(df)} valid coordinates from {Path(filename).absolute()}")

    clusters = clustering.cluster_locations(
        df=df, algorithm=algorithm, radius_km=distance, min_cluster_size=size
    )

    if not bool(clusters):
        click.secho("Did not find clusters matching input parameters.", fg="yellow")
        return

    print_debug(f"Found {len(clusters)} valid clusters using {algorithm}")

    encoded = encoding.encode_clusters(clusters)

    io.write_output_file(output, "result.txt", encoded["string"])
    io.write_output_file(output, "result.json", encoded["json"])
    io.write_output_file(output, "result.geojson", encoded["geojson"])

    vis = io.write_visualization(output, "result.html", encoded["geojson"])
    if vis is None:
        print_debug(f"Skipped generating visualization: kepler is not installed.")

    click.echo(f"Output files saved to {Path(output).absolute()}")

    if open:
        if vis:
            webbrowser.open_new_tab("file://" + str(vis.absolute()))
            print_debug(f"Opened visualization in default browser.")
        else:
            click.secho(
                "Can't open kepler.gl: package not installed. Please re-install geoclustering with `pip install geoclustering[full]`.",
                fg="yellow",
            )

    click.secho("Clustering completed.", fg="green")


if __name__ == "__main__":
    main()
