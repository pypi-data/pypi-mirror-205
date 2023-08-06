#!/usr/bin/python3

"""Creates a fingerprint circle of each training profile for visual comparison"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
import logging
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pyfsdb
import collections


def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: ",
    )

    parser.add_argument(
        "-s", "--size-labels", action="store_true", help="Add sizing labels"
    )

    parser.add_argument(
        "-b",
        "--missing-as-undef",
        action="store_true",
        help="If sizes are missing, don't drop them to zero just blank them",
    )

    parser.add_argument(
        "-v",
        "--violin-comparison",
        action="store_true",
        help="Use a violin plot for comparing multiple profiles",
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "input_file",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="Input training profile",
    )

    parser.add_argument("output_file", type=str, help="Output image file")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")
    return args


def create_fingerprint_plot(args, max_pkt_len, max_value, results):
    # create a figure and NxN subplots (with not all filled)
    num_plots = len(results) + 1
    nrows = int(np.sqrt(num_plots))
    if np.sqrt(num_plots) != nrows:
        nrows += 1
    ncols = nrows
    info(f"plot dimensions: {num_plots=} {nrows=} {ncols=}")
    fig, axes = plt.subplots(
        nrows=nrows, ncols=ncols, sharex=True, subplot_kw={"projection": "polar"}
    )

    # set various parameters on the first subplot

    labels = [0]
    for i in range(0, 8):
        labels.append(f"{int((i+1) * max_pkt_len/8)}")
    info(f"{max_pkt_len=}")
    info(f"{labels=}")

    max_axes_x = ncols - 1
    max_axes_y = nrows - 1

    for n, key in enumerate(results):
        r = []
        theta = []

        axes_x = int(n / ncols)
        axes_y = n % ncols

        for e_pkt_len in results[key]:
            theta.append(2 * np.pi * e_pkt_len / max_pkt_len)
            rv = 10 - np.abs(np.log10(results[key][e_pkt_len] / max_value))
            if not args.missing_as_undef and rv < -100:  # deal with inf
                rv = 0
            r.append(rv)

        colors = [
            "red",
            "green",
            "blue",
            "orange",
            "purple",
            "brown",
            "aqua",
            "teal",
            "darkblue",
            "greenyellow",
            "tomato",
            "saddlebrown",
            "magenta",
            "deeppink",
            "dodgerblue",
            "yellow",
            "olivedrab",
            "darkkhaki",
            "olive",
            "lightcoral",
            "firebrick",
            "steelblue",
            "mediumpurple",
            "navajowhite",
            "lawngreen",
            "gold",
            "sandybrown",
            "palegreen",
            "crimson",
            "darkgoldenrod",
        ]
        color = colors[n % len(colors)]
        info(f"color: {color}")

        info(f"{key:<20s} {theta[0:5]=}")
        info(f"{key:<20s} {theta[-5:]=}")
        info(f"{key:<20s} {r[0:5]=}")
        info(f"{key:<20s} {r[-5:]=}")
        axes[axes_x, axes_y].plot(theta, r, color=color)
        axes[max_axes_x, max_axes_y].plot(theta, r, color=color, alpha=0.3)
        axes[axes_x, axes_y].grid(True)
        axes[axes_x, axes_y].set_rticks([])
        if args.size_labels:
            axes[axes_x, axes_y].set_title(key, y=1.15)
            axes[axes_x, axes_y].set_xticklabels(labels)
        else:
            axes[axes_x, axes_y].set_title(key, y=1)
            axes[axes_x, axes_y].set_xticklabels([])

    # turn off all radial labeling
    for x in range(max_axes_x + 1):
        for y in range(max_axes_y + 1):
            axes[x, y].grid(True)
            axes[x, y].set_rticks([])

    # conglomerate title
    axes[max_axes_x, max_axes_y].set_title("All Protocols", y=1)

    fig.set_dpi(150)
    fig.set_size_inches(11, 7.5)
    # matplotlib.rcParams.update({'font.size': 10})

    hspace = 0.5
    if args.size_labels:
        hspace = 1.1
    plt.subplots_adjust(wspace=0, hspace=hspace)
    # save it to a file
    plt.tight_layout()
    plt.savefig(args.output_file)
    # or show it to the screen/console:
    # plt.show()


def create_violin_plot(args, max_pkt_len, max_value, results):
    # import seaborn as sns

    # create a figure and NxN subplots (with not all filled)
    num_plots = len(results)
    info(f"plot dimensions: {num_plots=}")
    fig, axes = plt.subplots(nrows=num_plots - 1, ncols=num_plots - 1)

    for n, key1 in enumerate(results):
        for m, key2 in enumerate(results):
            # drop things outside the plotting range
            if n - 1 < 0 or m >= len(results) - 1:
                continue

            # delete things in the upper right quad
            if n <= m and m < len(results) and n < len(results) and False:
                fig.delaxes(axes[n - 1, m])
                continue

            if n == m and m < len(results) and n < len(results):
                fig.delaxes(axes[n - 1, m])
                continue

            # create a difference array
            deltas = []
            for size in range(0, max_pkt_len):
                value = results[key1].get(size, 0) - results[key2].get(size, 0)
                deltas.append(value)

            debug(f"Plotting: {n}: {key1}, {m}: {key2} / {len(results)}")

            axes[n - 1, m].plot(range(0, 1500), deltas)
            #            axes[n-1, m].set_title(f"{key1}\nvs\n{key2}")
            axes[n - 1, m].set_xlim(0, max_pkt_len)
            axes[n - 1, m].set_ylim(-1.0, 1.0)
            if m == 0:
                axes[n - 1, m].set_ylabel(key1)
                axes[n - 1, m].spines.right.set_visible(False)
                axes[n - 1, m].spines.top.set_visible(False)
                # let the bottom left row have a x axis
                if n != len(results) - 1:
                    axes[n - 1, m].spines.bottom.set_visible(False)
                    axes[n - 1, m].set_xticklabels([])
                    axes[n - 1, m].set_xticks([])
                else:
                    axes[n - 1, m].set_xlabel(key2)
                    axes[n - 1, m].set_xticks([0, 500, 1000, 1500])
                    axes[n - 1, m].set_xticklabels([0, 500, 1000, 1500])
            elif n == len(results) - 1:
                axes[n - 1, m].set_xlabel(key2)
                axes[n - 1, m].spines.top.set_visible(False)
                axes[n - 1, m].spines.right.set_visible(False)
                axes[n - 1, m].spines.left.set_visible(False)
                axes[n - 1, m].set_yticklabels([])
                axes[n - 1, m].set_yticks([])
            else:
                # middle graphs get no decorations
                axes[n - 1, m].spines.top.set_visible(False)
                axes[n - 1, m].spines.right.set_visible(False)
                axes[n - 1, m].spines.left.set_visible(False)
                axes[n - 1, m].spines.bottom.set_visible(False)
                axes[n - 1, m].set_yticklabels([])
                axes[n - 1, m].set_yticks([])
                axes[n - 1, m].set_xticklabels([])
                axes[n - 1, m].set_xticks([])

            # axes[axes_x, axes_y].grid(True)
            # axes[axes_x, axes_y].set_rticks([])
            # if args.size_labels:
            #     axes[axes_x, axes_y].set_title(key, y=1.15)
            #     axes[axes_x, axes_y].set_xticklabels(labels)
            # else:
            #     axes[axes_x, axes_y].set_title(key, y=1)
            #     axes[axes_x, axes_y].set_xticklabels([])

    fig.set_dpi(150)
    fig.set_size_inches(11, 7.5)
    # matplotlib.rcParams.update({'font.size': 10})

    hspace = 0.5
    if args.size_labels:
        hspace = 1.1
    plt.subplots_adjust(wspace=0, hspace=hspace)
    # save it to a file
    plt.tight_layout()
    plt.savefig(args.output_file)
    # or show it to the screen/console:
    # plt.show()


def main():
    args = parse_args()

    results = collections.defaultdict(dict)
    max_pkt_len = 0
    max_value = 0
    with pyfsdb.Fsdb(
        file_handle=args.input_file, return_type=pyfsdb.RETURN_AS_DICTIONARY
    ) as inh:
        for row in inh:
            pkt_len = row["e_pkt_len"]
            max_pkt_len = max(pkt_len, max_pkt_len)
            for key in row:
                if key != "e_pkt_len":
                    results[key][pkt_len] = row[key]
                    max_value = max(row[key], max_value)

    if args.violin_comparison:
        create_violin_plot(args, max_pkt_len, max_value, results)
    else:
        create_fingerprint_plot(args, max_pkt_len, max_value, results)


if __name__ == "__main__":
    main()
