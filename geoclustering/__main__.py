import click
import webbrowser

import geoclustering.clustering as clustering
import geoclustering.encoding as encoding
import geoclustering.io as io


@click.command()
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
@click.argument("filename", type=click.Path(exists=True))
def main(distance, size, output, filename, algorithm):
    df = io.read_csv_file(filename)

    clusters = clustering.cluster_locations(
        df=df, algorithm=algorithm, radius_km=distance, min_cluster_size=size
    )

    if not bool(clusters):
        click.echo("Did not find clusters matching input parameters.")
        return

    encoded = encoding.encode_clusters(clusters)

    io.write_output_file(output, "result.txt", encoded["string"])
    io.write_output_file(output, "result.json", encoded["json"])
    io.write_output_file(output, "result.geojson", encoded["geojson"])
    vis = io.write_visualization(output, "result.html", encoded["geojson"])

    webbrowser.open_new_tab("file://" + str(vis.absolute()))


if __name__ == "__main__":
    main()
