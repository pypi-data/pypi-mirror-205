#!/usr/bin/python3

"""Imports a list of end-to-end tasks to do for training and
evaluation of pcaps for the rapid classifier."""

import os
import logging
import sys
import yaml
import pyfsdb
import collections
import traceback
import numpy as np
import time
import subprocess
import pkgutil
import shutil
import jinja2
import json
import datetime

from hashlib import sha256
from typing import Any, Union
from rich import print
from rich.console import Console
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
from concurrent.futures import ProcessPoolExecutor

# our modules
from apropos.goldminer.trainer import GoldMineTrainer
from apropos.goldminer.pickaxe.pickaxe import PickAxe
from apropos.goldminer.tools.aggregator import aggregate_results
from apropos.goldminer.tools.auditor import calculate_similarities, plot_similarities


def parse_args():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
        epilog="Exmaple Usage: ",
    )

    parser.add_argument(
        "--log-level",
        "--ll",
        default="info",
        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).",
    )

    parser.add_argument(
        "-c",
        "--config",
        default=[],
        nargs="*",
        help="name/value pairs of configuration to pass to override YAML properties",
    )

    parser.add_argument(
        "--train", action="store_true", help="Only conduct the training phase"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Conduct all parts (default if no other parts are specified)",
    )

    parser.add_argument("test_plan", type=str, help="Test plan to execute")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level, format="%(levelname)-10s:\t%(message)s")

    if not args.train:
        args.all = True

    return args


class TestAndEval:
    def __init__(self, default_algorithm="comparison", config_overrides={}):
        self.report_data = {"testing-graphs": {}}
        self.default_algorithm = default_algorithm
        self.config_overrides = config_overrides
        self.algorithm_results = {}
        self.label_map = None

    def read_test_plan(self, filename: str) -> dict:
        filehandle = open(filename)
        plan = yaml.safe_load(filehandle)

        # check for required main tokens
        for token in ["train", "test"]:
            if token not in plan:
                error(
                    f"required '{token}' keyword missing from plan file f{filehandle.name}"
                )
                exit(1)
        return plan

    def create_output_filename(
        self,
        starting_name: str,
        old_suffix: str = ".pcap",
        new_suffix: str = ".fsdb",
        output_directory=None,
    ):

        output_filename = starting_name
        if output_filename.endswith(old_suffix):
            output_filename = starting_name[: -len(old_suffix)]
        output_filename += new_suffix

        if output_directory:
            output_filename = os.path.basename(output_filename)
            output_filename = os.path.join(output_directory, output_filename)

        return output_filename

    def get_spec(
        self,
        plan: dict,
        sub_plan_component: dict,
        config_name: str,
        paths: Union[str, list[str]] = [],
        default: Any = None,
    ):

        # let the CLI override everything
        if config_name in self.config_overrides:
            try:
                return int(self.config_overrides[config_name])
            except Exception:
                return self.config_overrides[config_name]

        # if its in the deepest object, return that
        # TODO: check this
        if sub_plan_component and config_name in sub_plan_component:
            return sub_plan_component[config_name]

        # start searching downward
        if paths:
            if not isinstance(paths, list):
                paths = [paths]
            value = None

            # get the highest level as the  default
            if config_name in plan:
                value = plan[config_name]

            # recursively iterate down the paths for other values
            ptr = plan
            for path in paths:
                if path not in ptr:
                    break
                ptr = ptr[path]
                if config_name in ptr:
                    value = ptr[config_name]

            if value:
                return value

        if config_name in plan:
            return plan[config_name]

        return default

    def get_dist_file(self, filename, output_directory):
        "Copies a FILENAME found either local path or distribution install to OUTPUT_DIRECTORY"
        output_file = os.path.join(output_directory, filename)
        local_file = os.path.join("apropos/goldminer/reports", filename)
        if os.path.exists(local_file):
            shutil.copy(local_file, output_file)
        else:
            source_stream = pkgutil.get_data("apropos.goldminer.reports", filename)
            f = open(output_file, "wb")
            f.write(source_stream)
            f.close()
        return output_file

    def maybe_create_filtered_pcap(self, plan, plantype, spec):
        pkt_filter = self.get_spec(plan, spec, "filter", plantype, "")
        if not isinstance(pkt_filter, str) or pkt_filter == "":
            return

        tmpdir = self.get_spec(plan, spec, "tmp_dir", plantype, "/var/tmp")

        orig_file = spec["file"]
        new_hash = (
            sha256((orig_file + pkt_filter).encode("utf-8")).hexdigest() + ".pcap"
        )
        new_filename = os.path.join(tmpdir, new_hash)
        # count = self.get_spec(plan, spec, "packet_count", plantype, 0)

        if not os.path.exists(new_filename):
            info(f"filtering: {orig_file} with {pkt_filter=} to {new_filename}")
            subprocess.run(
                ["tcpdump", "-r", orig_file, "-w", new_filename, "-s", "0", pkt_filter]
            )
        else:
            debug(f" using filtered file: {orig_file} to {new_filename}")

        # fix the spec
        spec["original_file"] = spec["file"]
        spec["file"] = new_filename
        spec["filter_applied"] = pkt_filter
        if "filter" in spec:
            del spec["filter"]

    def process_training_item(self, trainspec, plan, output_directory):
        # build the trainer
        trainer = GoldMineTrainer(
            do_timing_analysis=plan["train"].get("no_timing", False),
            addresses=plan["train"].get("no_timing", None),
        )

        self.maybe_create_filtered_pcap(plan, "train", trainspec)

        filename = trainspec["file"]

        # analyze the files
        trainer.analyze_files(
            [filename],
            count=self.get_spec(plan, trainspec, "packet_count", "train", 0),
            pkt_filter=self.get_spec(plan, trainspec, "filter", "train"),
        )
        trainer.generate_results()

        # save the results as a parallel fsdb
        # TODO: allow saving to a different dir
        output_filename = self.create_output_filename(
            filename, output_directory=output_directory
        )

        debug(f"  saving to {output_filename}")
        trainer.output_to_fsdb(out_file_handle=open(output_filename, "w"))

        return {
            "results": trainer.results,
            "results_fsdb": output_filename,
            "label": trainspec["label"],
        }

    def create_training_set(
        self, plan: dict, output_directory: str = None, training_token: str = "train"
    ):
        results = {}
        labeled_pairs = []
        training_results = {}
        if not output_directory:
            output_directory = self.get_spec(plan, None, "output_directory")

        future_results = []
        info("starting training step")
        processes = plan.get("processes", 4)
        with ProcessPoolExecutor(processes) as executor:
            # load the process pool up with jobs
            for trainspec in plan[training_token]["files"]:
                future_result = executor.submit(
                    self.process_training_item, trainspec, plan, output_directory
                )
                future_results.append((trainspec, future_result))
                debug("submitted trainspec")

            # wait for all the results to finish
            info(f"created {len(future_results)} training")
            for n, training_pair in enumerate(future_results):
                (trainspec, future_result) = training_pair
                label = trainspec["label"]
                info(f"checking job {n} for {label} / {trainspec['file']}")
                try:
                    result = future_result.result()
                except Exception as ex:
                    error(f"training failed: {ex}")
                    error("".join(traceback.format_exc()))
                    exit()
                trainspec["results"] = result["results"]
                trainspec["results_fsdb"] = result["results_fsdb"]

                results[label] = result["results"]
                labeled_pairs.extend([label, result["results_fsdb"]])
                pkt_filter = self.get_spec(plan, trainspec, "filter")

                training_results[result["results_fsdb"]] = {
                    "profile": result["results"],
                    "filter": pkt_filter,
                    "label": result["label"],
                }

        # TODO: this is inefficient since we reload everything again
        # TODO: set this result file back in place if we calculate it?
        output_results = self.get_spec(
            plan, None, "results", default="training-profile.fsdb"
        )
        results_path = os.path.join(output_directory, output_results)
        plan["train"]["results"] = output_results
        plan["train"]["results_path"] = results_path

        # save the aggregated results
        debug(f"saving aggregated results to {output_results}")
        aggregate_results(labeled_pairs, open(results_path, "w"))
        self.report_data["training_results"] = training_results

    def calculate_training_similarities(self, plan):
        output_directory = self.get_spec(plan, None, "output_directory")

        labels = []
        for item in plan["train"]["files"]:
            labels.append(item["label"])

        do_not_normalize = plan["train"].get("do_not_normalize", False)

        debug(f"calculating similarities from {plan['train']['results']}")
        (types, similiarities) = calculate_similarities(
            open(plan["train"]["results_path"]),
            labels,
            do_not_normalize=do_not_normalize,
        )

        if "similarity" not in plan["train"]:
            plan["train"]["similarity"] = "training-similarity.png"
            plan["train"]["similarity_path"] = os.path.join(
                output_directory, "training-similarity.png"
            )

        self.report_data["similarities"] = plan["train"]["similarity"]
        info(f"plotting similarities to {plan['train']['similarity']}")
        plot_similarities(types, similiarities, plan["train"]["similarity_path"])

    def create_graph(self, output_file, test):
        output_graph_file = self.create_output_filename(
            output_file, old_suffix=".fsdb", new_suffix=".png"
        )
        output_graph_basename = os.path.basename(output_graph_file)
        import multikeygraph

        graph_source = test.get("original_file", test["file"])

        try:
            m = multikeygraph.MultiKeyGraph()
            info(f"opening output graph of {output_file}")
            m.graph(
                [open(output_file)],
                columns=["confidence"],
                time_column="timestamp",
                key_column="token",
                title=f"Detection graph for {test['label']}: {graph_source}",
                scatter=True,
                line_width=5,
                output_file=output_graph_file,
            )
            info(f"  finished output graph of {output_file}")
            return output_graph_file
        except Exception:
            warning(f"failed to produce a graph for {output_file}")
            warning("".join(traceback.format_exc()))

    def maybe_relabel(self, plan, label):
        """Potentially returns an aggregate label according to a specified label
        mapping from the plan"""
        if not self.label_map:
            self.label_map = self.get_spec(plan, None, "label_map")
        if self.label_map and label in self.label_map:
            return self.label_map[label]
        return label

    def run_single_test(
        self,
        plan,
        labels,
        output_directory,
        test,
        test_num: int,
        generate_graph: bool = True,
        training_token: str = "train",
        testing_token: str = "test",
    ):
        axe = PickAxe(
            gold_profiles=labels,
            training_data_file=plan[training_token]["results_path"],
            # support_windowing=args.window_analysis
        )
        axe.algorithm = self.get_spec(
            plan, test, "algorithm", testing_token, "comparison"
        )
        axe.label_map = self.get_spec(plan, test, "label_map", testing_token)

        self.maybe_create_filtered_pcap(plan, testing_token, test)

        if "output" in test:
            output_file = os.path.join(output_directory, test["output"])
        else:
            output_file = self.create_output_filename(
                test["file"],
                old_suffix=".pcap",
                new_suffix=f".test.{test_num}.fsdb",
                output_directory=output_directory,
            )
        debug(f"  output results:  {test['file']} => {output_file}")
        # default to FSDB output formatted
        from apropos.goldminer.output.goldFsdb import GoldFsdb

        axe.output = GoldFsdb(out_file=output_file, save_values=True)

        packet_count = self.get_spec(plan, test, "packet_count", testing_token, 0)
        axe.three_tuple_only = self.get_spec(
            plan, test, "three_tuple_only", testing_token, False
        )

        t_start = time.time()
        (identifiers, counts, processed_data) = axe.process_pcap(
            test["file"],
            pkt_filter=self.get_spec(plan, test, "filter", testing_token),
            max_packets=packet_count,
            skip_packets=self.get_spec(plan, test, "skip_packets", testing_token, 0),
        )

        axe.close()
        t_end = time.time()

        output_graph_file = "broken.png"
        if generate_graph:
            if not os.path.exists(output_file) or os.path.getsize(output_file) < 5:
                warning(
                    "output FSDB file {output_file} is missing or too small -- not graphing"
                )
            else:
                if os.path.getsize(output_file) > 0:
                    if False:
                        self.create_graph(output_file, test)
                else:
                    warning(f"{output_file} too small")

        return (
            test,
            identifiers,
            counts,
            processed_data,
            axe.output.save_values,
            output_file,
            output_graph_file,
            test["file"],
            t_end - t_start,
        )

    def run_test_set(self, plan: dict, testing_token: str = "test"):
        output_directory = self.get_spec(plan, plan[testing_token], "output_directory")

        labels = []
        for test in plan[testing_token]["files"]:
            labels.append(test["label"])

        future_results = []
        info("starting testing step")

        # remember the default algorithm
        self.algorithm = plan.get("algorithm", self.default_algorithm)
        self.report_data["algorithm_used"] = self.algorithm

        output_results = []
        self.saved_results = []
        processes = plan.get("processes", 4)

        with ProcessPoolExecutor(processes) as executor:
            # buil the pool of tests
            for n, test in enumerate(plan[testing_token]["files"]):

                alg = self.get_spec(
                    plan, test, "algorithm", testing_token, "comparison"
                )

                future_result = executor.submit(
                    self.run_single_test, plan, labels, output_directory, test, n
                )
                future_results.append((test["file"], future_result, test["label"]))
            info(f"created {len(future_results)} test jobs")

            # wait for all the results
            import pdb

            for n, packed_future in enumerate(future_results):
                (file, future_result, label) = packed_future
                info(f"checking job {n} for {label} / {file}")
                result = future_result.result()
                (
                    test,
                    identifiers,
                    counts,
                    processed_data,
                    save_values,
                    output_file,
                    output_graph_file,
                    filtered_file,
                    time_delta,
                ) = result
                output_graph_file = self.create_graph(output_file, test)
                if output_graph_file == None:
                    output_graph_file = "broken.png"
                # FIX: something goes wrong when this is in a thread:
                total_count = sum(counts.values())
                self.saved_results.append(
                    {
                        "test_specification": test,
                        "results": save_values,
                        "file": file,
                        "label": label,
                        "mapped_label": self.maybe_relabel(plan, label),
                        "graph": os.path.basename(output_graph_file),
                        "graph_path": output_graph_file,
                        "filtered": filtered_file,
                        "processing_time": f"{time_delta/60.0:0.4f}",
                        "identifier_counts": dict(counts),
                        "total_count": total_count,
                    }
                )

        self.report_data["test_results"] = self.saved_results
        self.report_data["processes"] = processes

    def print_results(self, plan, output_directory=None):
        console = Console()

        # print the analysis per file
        console.print("state {:<50} {:<20} {}".format("Identifier", "label", "value"))

        bytrace_results = collections.defaultdict(collections.Counter)
        self.count_results = bytrace_results

        pair_results = collections.defaultdict(collections.Counter)
        self.pair_results = pair_results

        bytype_results = collections.defaultdict(collections.Counter)
        self.bytype_results = bytype_results

        self.report_data["bytype_results"] = bytype_results
        self.report_data["bytrace_results"] = bytrace_results

        for saved_result in self.saved_results:
            file = saved_result["file"]
            trace_label = saved_result["mapped_label"]
            results = saved_result["results"]
            filtered = saved_result["filtered"]
            print(f"---- {trace_label:<20} {file}")
            if filtered != file:
                print(f"   {filtered=}")

            if len(results) == 0:
                warning("No identifier found in results for {filtered=}")
            for identifier in results:
                max_val = -100
                best_label = None
                for label in results[identifier]:
                    label = self.maybe_relabel(plan, label)
                    if results[identifier][label] > max_val:
                        max_val = results[identifier][label]
                        best_label = label
                        if best_label == trace_label:
                            determination = "good"
                            style = "green"
                            tp_fp_label = label
                        else:
                            determination = "bad"
                            style = "red"
                            tp_fp_label = "others"
                console.print(f"{determination:<4} ", style=style, end="")
                import pdb

                print(f"{str(identifier):<50} {best_label:<20} {max_val}")

                # count by trace
                bytrace_results[trace_label][determination] += 1

                # count by classifier type
                bytype_results[best_label][determination] += 1

                # remember pairings of trace_type and classifier_type
                pair_results[trace_label][best_label + "_" + determination] += 1

                if determination == "bad":
                    pair_results[trace_label]["others_bad"] += 1

            # print the summary analysis of each file during its file output
            print("               tp  fp  precision".format(key="Input type"))

            if (
                bytrace_results[trace_label]["good"] == 0
                and bytrace_results[trace_label]["bad"] == 0
            ):
                print(f"    PRECISION: broken!  no results")
            else:
                precision = bytrace_results[trace_label]["good"] / (
                    bytrace_results[trace_label]["good"]
                    + bytrace_results[trace_label]["bad"]
                )
                print(
                    f"   PRECISION: {bytrace_results[trace_label]['good']:>3} {bytrace_results[trace_label]['bad']:>3}  {precision:<0.3}"
                )

        # print the summary analysis of each detector
        print("=" * 60)
        console.print("RESULTS BY TYPE", style="blue")
        print("{key:<50} tp  fp  precision".format(key="Detector"))
        for key in bytype_results:
            precision = bytype_results[key]["good"] / (
                bytype_results[key]["good"] + bytype_results[key]["bad"]
            )
            print(
                f"{key:<50} {bytype_results[key]['good']:<3} {bytype_results[key]['bad']:<3} {precision:<0.3}"
            )
            bytype_results[key]["percent"] = precision

        if output_directory:
            self.save_results(
                output_directory, bytrace_results, bytype_results, pair_results
            )

    def save_results(
        self, output_directory, bytrace_results, bytype_results, pair_results
    ):
        with pyfsdb.Fsdb(out_file=os.path.join(output_directory, "results.fsdb")) as fh:
            # extract keys
            trace_keys = list(bytrace_results.keys())
            classifier_keys = list(bytype_results.keys())

            first_trace_key = list(pair_results.keys())[0]
            other_keys = classifier_keys
            out_column_names = ["traffic_label"]
            for key in classifier_keys:
                out_column_names.append(key + "_true")
                out_column_names.append(key + "_false")
                out_column_names.append(key + "_precision")
            fh.out_column_names = out_column_names

            # add data
            for traffic_type in pair_results:
                out = [traffic_type]
                others_bad = pair_results[traffic_type]["others_bad"]
                # TODO: requires traffic_type always be a classifier
                good = pair_results[traffic_type].get(traffic_type + "_good", 0)

                # find the precision for the proper detector
                precision = 0.0
                if good + others_bad != 0:
                    precision = float(good) / float(good + others_bad)
                pair_results[traffic_type][traffic_type + "_precision"] = precision

                # find the false discovery rates for other keys
                for key in classifier_keys:
                    if key == traffic_type:
                        # skip what we calculated above already
                        continue

                    # how many did this classifier mislabel for this traffic
                    bad = pair_results[traffic_type].get(key + "_bad", 0)

                    # FDR = FP / (TP + FP)
                    false_discovery_rate = 0.0
                    if good + bad != 0:
                        false_discovery_rate = float(bad) / float(good + bad)
                    pair_results[traffic_type][
                        key + "_false_discovery_rate"
                    ] = false_discovery_rate
                    out.extend([good, others_bad, precision, false_discovery_rate])
                fh.append(out)

    def create_roc_curves(self, plan, output_directory):
        """Creates a ROC curve for the results

        Currently this only generates the ROC curve for ALL results

        TODO Eventually:
        - per classifier
        - per data source type
        """

        from roc_utils import compute_roc, plot_roc

        saved_results = self.report_data["test_results"]

        # clear out previous plots
        import matplotlib.pyplot as plt

        plt.clf()
        plt.cla()
        plt.close()

        # build a complete roc curve set for *all* data
        all_trues = []
        all_confidences = []

        classifier_trues = collections.defaultdict(list)
        classifier_confidences = collections.defaultdict(list)
        for test_result in saved_results:
            truth_label = self.maybe_relabel(plan, test_result["label"])
            for identifier in test_result["results"]:
                for classifier_label in test_result["results"][identifier]:
                    classifier_label = self.maybe_relabel(plan, classifier_label)
                    if truth_label == classifier_label:
                        all_trues.append(1)
                        classifier_trues[classifier_label].append(1)
                    else:
                        all_trues.append(0)
                        classifier_trues[classifier_label].append(0)
                    all_confidences.append(
                        test_result["results"][identifier][classifier_label]
                    )
                    classifier_confidences[classifier_label].append(
                        test_result["results"][identifier][classifier_label]
                    )

        roc = compute_roc(all_confidences, all_trues, pos_label=1)
        plot_roc(roc, label="All Results")
        all_auc = roc.auc
        self.report_data["test_auc"] = f"{all_auc:0.4f}"
        plt.savefig(os.path.join(output_directory, "results-ROC.png"))
        plt.clf()
        plt.cla()
        plt.close()

        self.report_data["test_auc_classifiers"] = {}
        for classifier_label in classifier_trues:
            classifier_label = self.maybe_relabel(plan, classifier_label)
            roc = compute_roc(
                classifier_confidences[classifier_label],
                classifier_trues[classifier_label],
                pos_label=1,
            )
            plot_roc(roc, label=f"classifier {classifier_label}")
            auc_result = roc.auc
            self.report_data["test_auc_classifiers"][
                classifier_label
            ] = f"{auc_result:0.4f}"
            plt.savefig(
                os.path.join(output_directory, f"results-{classifier_label}-ROC.png")
            )
            plt.clf()
            plt.cla()
            plt.close()

    def create_heat_map(self, output_filename):
        import matplotlib.pyplot as plt

        # generate the graph
        fig, ax = plt.subplots()

        # set the size
        fig.set_dpi(150)
        fig.set_size_inches(16, 9)

        data = []
        trace_keys = list(self.pair_results.keys())
        classifier_keys = trace_keys  # TODO: could be different

        # create the data to plot
        print(self.pair_results)

        for classifier in classifier_keys:
            row = []
            data.append(row)
            for trace in trace_keys:
                if classifier == trace:
                    row.append(self.pair_results[trace][classifier + "_precision"])
                else:
                    row.append(
                        self.pair_results[trace][classifier + "_false_discovery_rate"]
                    )

                # for the cool-warm colormap, we want good values to be negative (cool)
                # so that bad values are warm/red (hot)
                if trace == classifier:
                    row[-1] = -row[-1]  # negative for matching/good rows
                else:
                    pass

        # add trace keys as labels
        ax.set_title(f"algorithm: {self.default_algorithm}")
        label_size = 14
        ax.set_yticks(np.arange(len(trace_keys)))
        ax.set_yticklabels(trace_keys, fontsize=label_size)

        ax.set_xticks(np.arange(len(classifier_keys)))
        ax.set_xticklabels(classifier_keys, fontsize=label_size)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # TODO: accept cmap as option -- bwr is also good
        ax.imshow(data, vmin=-1.0, vmax=1.0, cmap="seismic")
        ax.set_xlabel("traffic type", fontsize=label_size)
        ax.set_ylabel("classifier", fontsize=label_size)

        for x, row in enumerate(data):
            for y, value in enumerate(row):
                if data[x][y] != 0.0:
                    label = "FDR: \n"
                    if x == y:
                        label = "TPR: \n"
                    ax.text(
                        y,
                        x,
                        f"{label}{abs(value):1.1f}",
                        ha="center",
                        va="center",
                        color="#ffff00",
                        fontsize=label_size,
                    )

        fig.tight_layout()

        fig.savefig(output_filename, bbox_inches="tight", pad_inches=0)
        plt.clf()
        plt.cla()
        plt.close()

    def get_support_files(self, output_directory):
        # supporting files
        for support in [
            "template.html",
            "navbar.html",
            "navbar-summary.html",
            "header.html",
            "report.css",
            "hardhat.svg",
            "cancel.svg",
            "check.svg",
        ]:
            self.get_dist_file(support, output_directory)

    def create_report(self, plan, output_directory=None):
        "Creates a markdown report based on the data from the training and tests"

        report_name = self.get_spec(
            plan, None, "report_name", "report", "evaluation-report.md"
        )
        report_name = os.path.join(output_directory, report_name)

        template = self.get_dist_file("template.md", output_directory)
        template_contents = open(template, "r").read()

        # mark results as all good, or not
        for testcase in self.report_data["test_results"]:
            truth_label = self.maybe_relabel(
                plan, testcase["test_specification"]["label"]
            )
            all_true = True
            for identifier in testcase["results"]:
                labels = sorted(
                    testcase["results"][identifier],
                    key=lambda x: testcase["results"][identifier][x],
                    reverse=True,
                )
                if labels[0] != truth_label:
                    all_true = False
                testcase["success"] = labels[0] == truth_label
            testcase["all_true"] = all_true

        self.get_support_files(output_directory)

        info(f"creating report {report_name}")
        md = open(report_name, "w")

        jinja_template = template_contents
        loader = jinja2.FileSystemLoader("./")
        env = jinja2.Environment(loader=loader)
        template = env.from_string(jinja_template)

        md.write(template.render(self.report_data) + "\n")
        md.close()

    def generate_summary_report(self, plan, output_directory, algorithm_results):
        self.get_support_files(output_directory)

        template = self.get_dist_file("summary-template.md", output_directory)
        template_contents = open(template, "r").read()

        report_name = self.get_spec(
            plan, None, "summary_name", "report", "summary-report.md"
        )
        report_name = os.path.join(output_directory, report_name)

        info(f"creating summary {report_name}")
        md = open(report_name, "w")

        jinja_template = template_contents
        loader = jinja2.FileSystemLoader("./")
        env = jinja2.Environment(loader=loader)
        template = env.from_string(jinja_template)

        report_data = {
            "algorithm_results": algorithm_results,
            "output_directory": output_directory,
        }
        md.write(template.render(report_data) + "\n")
        md.close()

    def generate_html_report(
        self,
        output_directory,
        input_template: str = "evaluation-report.md",
        output_file: str = "index.html",
        navbar: str = "navbar.html",
    ):
        tmpfile = f"{output_directory}/report_tmp.html"

        # run pandoc
        cmd = [
            "pandoc",
            # "--verbose",
            "--log=DEBUG.txt",
            "-i",
            f"{output_directory}/{input_template}",
            "-o",
            tmpfile,
            "",
            "--template",
            f"{output_directory}/template.html",
            "--include-in-header",
            f"{output_directory}/header.html",
            "--include-before-body",
            f"{output_directory}/{navbar}",
            "--standalone",
            "--toc",
            "--toc-depth",
            "2",
            "--metadata",
            "title=gold-miner-report",
        ]
        debug("running: " + " ".join(cmd))
        subprocess.run(["bash", "-c", " ".join(cmd)])

        # filter resulting html
        with open(tmpfile) as inh:
            with open(f"{output_directory}/{output_file}", "w") as outh:
                for line in inh:
                    if line.startswith("<p><img"):
                        line = line.replace("<img ", '<img class="img-fluid" ')
                    line = line.replace(
                        "gold-miner-report", "Gold-Mine Test and Evaluation Report"
                    )
                    outh.write(line)

        os.unlink(tmpfile)
        info(f"creating {output_directory}/{output_file}")

    def dump_algorithm_results(
        self, output_directory: str, output_filename: str = "results.json"
    ):
        data = {}
        for key in (
            "processes",
            "tande_time",
            "test_auc",
            "test_auc_classifiers",
            "algorithm_used",
        ):
            data[key] = self.report_data[key]
        json.dump(data, open(os.path.join(output_directory, output_filename), "w"))
        self.algorithm_results[self.report_data["algorithm_used"]] = data


def main():
    args = parse_args()

    config_overrides = {}
    for pair in args.config:
        (key, value) = pair.split("=")
        key = key.strip()
        value = value.strip()
        config_overrides[key] = value

    tande = TestAndEval(config_overrides=config_overrides)
    plan = tande.read_test_plan(args.test_plan)
    default_algorithm = tande.get_spec(plan, None, "algorithm", default="comparison")
    algorithms = [default_algorithm]
    orig_output_directory = tande.get_spec(plan, None, "output_directory")

    if default_algorithm == "all":
        algorithms = PickAxe().algorithms

    algorithm_results = {}
    for algorithm in algorithms:
        tande = TestAndEval(config_overrides=config_overrides)
        plan = tande.read_test_plan(args.test_plan)

        tande.algorithm = algorithm
        plan["algorithm"] = algorithm
        output_directory = orig_output_directory
        if len(algorithms) > 1:
            output_directory = os.path.join(output_directory, algorithm)
            plan["output_directory"] = output_directory

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        start_time = time.time()
        tande.create_training_set(plan)
        tande.calculate_training_similarities(plan)
        tande.run_test_set(plan)
        end_time = time.time()

        tande.report_data["tande_time"] = f"{(end_time - start_time) / 60.0:0.4f}"

        tande.print_results(plan, output_directory)
        tande.create_roc_curves(plan, output_directory)
        tande.create_heat_map(os.path.join(output_directory, "comparison.png"))
        tande.create_report(plan, output_directory)
        tande.dump_algorithm_results(output_directory)

        tande.generate_html_report(output_directory)

        shutil.copy(
            args.test_plan,
            os.path.join(output_directory, os.path.basename(args.test_plan)),
        )

        algorithm_results[algorithm] = tande.algorithm_results[algorithm]

    if len(algorithms) > 1:
        tande.generate_summary_report(plan, orig_output_directory, algorithm_results)
        tande.generate_html_report(
            orig_output_directory,
            input_template="summary-report.md",
            navbar=f"{algorithms[0]}/navbar-summary.html",
        )

    console = Console()
    console.print("")
    console.print("-----------------------", style="green")
    console.print(f"output directory: '{output_directory}'")
    console.print(f"  report:         '{output_directory}/index.html'")


if __name__ == "__main__":
    main()
