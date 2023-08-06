#!/usr/bin/python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyfsdb
import json

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import error
import sys

try:
    from rich import print
except Exception:
    pass


def parse_args():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: ./create-comparison [-t types] -- infile outfile",
    )

    parser.add_argument(
        "-t",
        "--types",
        nargs="*",
        default=[],
        help="Types to compare -- if none are specified, all data keys will be used",
    )

    parser.add_argument(
        "-d",
        "--distances-for",
        default=None,
        type=str,
        nargs="*",
        help="Describe distances from a given type",
    )

    parser.add_argument(
        "-D",
        "--distances-all",
        action="store_true",
        help="Describe distances for every type",
    )

    parser.add_argument(
        "-g",
        "--determine-good",
        action="store_true",
        help="Describe good/bad estimations instead of distances",
    )

    parser.add_argument(
        "-n",
        "--do-not-normalize",
        action="store_true",
        help="Don't normalize the distance output (only useful with -d)",
    )

    parser.add_argument(
        "-j", "--json", action="store_true", help="Use JSON output when possible"
    )

    parser.add_argument(
        "-f", "--fsdb", action="store_true", help="Use FSDB output when possible"
    )

    parser.add_argument(
        "input_file",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="Combined input files with a column per type",
    )

    parser.add_argument(
        "output_file", type=str, nargs="?", help="Where to save the resulting png"
    )

    args = parser.parse_args()

    if not args.output_file and not args.distances_for:
        error("Either an output image file or -d is required")
        exit(1)

    return args


def calculate_similarities(
    input_file, labels: list = None, do_not_normalize: bool = False
):
    f = pyfsdb.Fsdb(file_handle=input_file, return_type=pyfsdb.RETURN_AS_DICTIONARY)
    data = f.get_all()

    if not labels:
        columns = f.column_names
        labels = columns[1:]  # drop the packet size column

    maxv = -1
    minv = 1000
    similarities = []
    # calculate the similiar vs each other
    for i, it in enumerate(labels):
        similarities.append([])
        for j, jt in enumerate(labels):
            difference = 0.0
            for n, values in enumerate(data):
                iv = values[it]
                jv = values[jt]

                if iv == "-":
                    iv = 0.0
                if jv == "-":
                    jv = 0.0

                difference += abs(float(iv) - float(jv))

            maxv = max(maxv, difference)
            minv = min(minv, difference)

            similarities[i].append(difference)

    if not do_not_normalize:
        for i in range(len(similarities)):
            for j in range(len(similarities[i])):
                similarities[i][j] /= maxv

    return (labels, similarities)


def plot_similarities(types: list, similarities: list, output_file):
    # https://matplotlib.org/3.2.2/gallery/images_contours_and_fields/image_annotated_heatmap.html
    fig, ax = plt.subplots()
    im = ax.imshow(np.array(similarities))

    ax.set_title("Differentiability between protocols")

    ax.set_xticks(np.arange(len(types)))
    ax.set_xticklabels(types)
    ax.set_yticks(np.arange(len(types)))
    ax.set_yticklabels(types)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(similarities)):
        for j in range(len(similarities)):
            text = ax.text(
                j,
                i,
                "{:1.1f}".format(similarities[i][j]),
                ha="center",
                va="center",
                color="w",
            )

    fig.tight_layout()
    plt.savefig(output_file, bbox_inches="tight", pad_inches=0)

    # https://www.tutorialspoint.com/plotly/plotly_heatmap.htm
    #   - didn't work -- orca installation problematic
    # data = go.Heatmap(x=types, y=types, z=np.array(similiarities), type='heatmap')
    # fig = go.Figure(data = data)
    # fig.write_image(file="analysis_results/matrix.png", format='png')


def describe_type(
    describe_type: str, types: list, similiarities: list, just_return_data=False
):
    "prints a table of other protocols and their similarity"
    index = types.index(describe_type)
    selection = sorted(zip(types, similiarities[index]), key=lambda x: x[1])

    if not just_return_data:
        print(f"Similarity distance (lower is more similar) for '{describe_type}':")
        print("")

    if just_return_data:
        return list(selection)

    for item in selection:
        if item[0] == describe_type:
            continue
        print("  {:<40} {:,.3f}".format(item[0], item[1]))
    print("")


fsdb_handle = None


def determine_best(
    describe_type: str,
    types: list,
    similiarities: list,
    use_json: bool = False,
    use_fsdb: bool = False,
):
    "displays which other protocols it is most likely successful at detecting"
    index = types.index(describe_type)
    selection = sorted(zip(types, similiarities[index]), key=lambda x: x[1])

    # goal: find the knee in the curve where the difference is suddenly large
    # path: take the derivate and the maximum value in it as the point to stop at

    last_value = similiarities[0][0]
    max_delta = 0
    selection = list(map(list, selection))  # was tuples
    index = 0
    for n, item in enumerate(selection):
        value = float(item[1]) - last_value
        item.append(value)
        if value > max_delta:
            max_delta = value
            index = n
        last_value = float(item[1])

    goods = set([x[0] for x in selection[:index]])
    goods.discard(describe_type)
    if use_json:
        print(
            json.dumps({"good": goods, "unlikely": [x[0] for x in selection[index:]]})
        )
    elif use_fsdb:
        global fsdb_handle
        if not fsdb_handle:
            fsdb_handle = pyfsdb.Fsdb(out_file_handle=sys.stdout)
            fsdb_handle.out_column_names = [""]
    else:
        good = ", ".join(goods)
        unlikely = ", ".join([x[0] for x in selection[index:]])

        print(f"Good:     {good}")
        print(f"Unlikely: {unlikely}")


def main():
    args = parse_args()
    (types, similiarities) = calculate_similarities(
        args.input_file, args.types, do_not_normalize=args.do_not_normalize
    )
    if args.output_file:
        plot_similarities(types, similiarities, args.output_file)

    if args.distances_all:
        args.distances_for = types

    if args.distances_for:
        container = {}
        for distance_for in args.distances_for:
            if args.determine_good:
                determine_best(distance_for, types, similiarities, use_json=args.json)
            else:
                container[distance_for] = describe_type(
                    distance_for, types, similiarities, just_return_data=args.json
                )

        if args.json and args.distances_for and not args.determine_good:
            print(json.dumps(container))


if __name__ == "__main__":
    main()
