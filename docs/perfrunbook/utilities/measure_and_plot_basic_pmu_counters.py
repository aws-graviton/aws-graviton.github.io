#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import numpy as np
import re
from scipy import stats
import subprocess
import io

# When calculating aggregate stats, if some are zero, may
# get a benign divide-by-zero warning from numpy, make it silent.
np.seterr(divide='ignore')


def perfstat(time, period, cpus, counter_numerator, counter_denominator, __unused__):
    """
    Measure performance counters using perf-stat in a subprocess.  Return a CSV buffer of the values measured.
    """
    try:
        if not cpus:
            res = subprocess.run(["lscpu", "-p=CPU"], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = io.StringIO(res.stdout.decode('utf-8'))
            cpus = []
            for line in output.readlines():
                match = re.search(r'''^(\d+)$''', line)
                if match is not None:
                    cpus.append(match.group(1))

        res = subprocess.run(["perf", "stat", f"-C{','.join(cpus)}", f"-I{period}", "-x|", "-a", "-e", f"{counter_numerator}", "-e", f"{counter_denominator}", "--", "sleep", f"{time}"],
                             check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return io.StringIO(res.stdout.decode('utf-8'))
    except subprocess.CalledProcessError:
        print("Failed to measure performance counters.")
        print("Please check that perf is installed using install_perfrunbook_dependencies.sh and in your PATH")
        return None


def plot_terminal(data, title, xtitle):
    """
    Plot data to the terminal using plotext
    """
    import plotext as plt
    x = data.index.tolist()
    y = data[title].tolist()

    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(xtitle)
    plt.plot_size(100, 30)
    plt.show()


def plot_counter_stat(csv, logfile, plot, stat_name, counter_numerator,
                      counter_denominator, scale):
    """
    Process the returned csv file into a time-series statistic to plot and
    also calculate some useful aggregate stats.
    """
    df = pd.read_csv(csv, sep='|',
                     names=['time', 'count', 'rsrvd1', 'event',
                            'rsrvd2', 'frac', 'rsrvd3', 'rsrvd4'],
                     dtype={'time': np.float64, 'count': np.float64,
                            'rsrvd1': str, 'event': str, 'rsrvd2': str,
                            'frac': np.float64, 'rsrvd3': str, 'rsrvd4': str})
    df_processed = pd.DataFrame()

    df_processed[stat_name] = (df[df['event'] == counter_numerator]['count'].reset_index(drop=True)) / (df[df['event'] == counter_denominator]['count'].reset_index(drop=True)) * scale
    df_processed[counter_numerator] = df[df['event'] == counter_numerator]['count'].reset_index(drop=True)
    df_processed[counter_denominator] = df[df['event'] == counter_denominator]['count'].reset_index(drop=True)
    df_processed.dropna(inplace=True)

    # Calculate some meaningful aggregate stats for comparing time-series plots
    geomean = stats.gmean(df_processed[stat_name])
    p50 = stats.scoreatpercentile(df_processed[stat_name], 50)
    p90 = stats.scoreatpercentile(df_processed[stat_name], 90)
    p99 = stats.scoreatpercentile(df_processed[stat_name], 99)
    xtitle = f"gmean:{geomean:>6.2f} p50:{p50:>6.2f} p90:{p90:>6.2f} p99:{p99:>6.2f}"

    if logfile:
        df_processed.to_csv(logfile)
    if plot:
        plot_terminal(df_processed, stat_name, xtitle)


def get_cpu_type():
    GRAVITON_MAPPING = {
        "0xd0c": "Graviton2",
        "0xd40": "Graviton3",
        "0xd4f": "Graviton4"
    }
    AMD_MAPPING = {
        "7R13": "Milan",
        "9R14": "Genoa"
    }

    with open("/proc/cpuinfo", "r") as f:
        for line in f.readlines():
            if "model name" in line:
                ln = line.split(":")[-1].strip()
                if "AMD EPYC" in ln:
                    # Return the model number of the AMD CPU, its the 3rd entry in format
                    # AMD EPYC <model>
                    return AMD_MAPPING[ln.split(" ")[2]]
                else:
                    return ln
            elif "CPU part" in line:
                cpu = line.split(":")[-1].strip()
                return GRAVITON_MAPPING[cpu]


UNIVERSAL_GRAVITON_CTRS = {
    "ipc": ["armv8_pmuv3_0/event=0x8/", "armv8_pmuv3_0/event=0x11/", 1],
    "branch-mpki": ["armv8_pmuv3_0/event=0x10/", "armv8_pmuv3_0/event=0x8/", 1000],
    "data-l1-mpki": ["armv8_pmuv3_0/event=0x3/", "armv8_pmuv3_0/event=0x8/", 1000],
    "inst-l1-mpki": ["armv8_pmuv3_0/event=0x1/", "armv8_pmuv3_0/event=0x8/", 1000],
    "l2-mpki": ["armv8_pmuv3_0/event=0x17/", "armv8_pmuv3_0/event=0x8/", 1000],
    "l3-mpki": ["armv8_pmuv3_0/event=0x37/", "armv8_pmuv3_0/event=0x8/", 1000],
    "stall_frontend_pkc": ["armv8_pmuv3_0/event=0x23/", "armv8_pmuv3_0/event=0x11/", 1000],
    "stall_backend_pkc": ["armv8_pmuv3_0/event=0x24/", "armv8_pmuv3_0/event=0x11/", 1000],
    "inst-tlb-mpki": ["armv8_pmuv3_0/event=0x2/", "armv8_pmuv3_0/event=0x8/", 1000],
    "inst-tlb-tw-pki": ["armv8_pmuv3_0/event=0x35/", "armv8_pmuv3_0/event=0x8/", 1000],
    "data-tlb-mpki": ["armv8_pmuv3_0/event=0x5/", "armv8_pmuv3_0/event=0x8/", 1000],
    "data-tlb-tw-pki": ["armv8_pmuv3_0/event=0x34/", "armv8_pmuv3_0/event=0x8/", 1000],
    "code-sparsity": ["armv8_pmuv3_0/event=0x11c/", "armv8_pmuv3_0/event=0x8/", 1000],
}
GRAVITON3_CTRS = {
    "stall_backend_mem_pkc": ["armv8_pmuv3_0/event=0x4005/", "armv8_pmuv3_0/event=0x11/", 1000],
}
UNIVERSAL_INTEL_CTRS = {
    "ipc": ["cpu/event=0xc0,umask=0x0/", "cpu/event=0x3c,umask=0x0/", 1],
    "branch-mpki": ["cpu/event=0xC5,umask=0x0/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-l1-mpki": ["cpu/event=0x51,umask=0x1/", "cpu/event=0xc0,umask=0x0/", 1000],
    "inst-l1-mpki": ["cpu/event=0x24,umask=0xe4/", "cpu/event=0xc0,umask=0x0/", 1000],
    "l2-mpki": ["cpu/event=0xf1,umask=0x1f/", "cpu/event=0xc0,umask=0x0/", 1000],
    "l3-mpki": ["cpu/event=0x2e,umask=0x41/", "cpu/event=0xc0,umask=0x0/", 1000],
    "stall_frontend_pkc": ["cpu/event=0x9C,umask=0x1,cmask=0x4/", "cpu/event=0x3c,umask=0x0/", 1000],
    "stall_backend_pkc": ["cpu/event=0xA2,umask=0x1/", "cpu/event=0x3c,umask=0x0/", 1000],
    "inst-tlb-mpki": ["cpu/event=0x85,umask=0x20/", "cpu/event=0xc0,umask=0x0/", 1000],
    "inst-tlb-tw-pki": ["cpu/event=0x85,umask=0x01/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-tlb-mpki": ["cpu/event=0x08,umask=0x20/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-st-tlb-mpki": ["cpu/event=0x49,umask=0x20/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-tlb-tw-pki": ["cpu/event=0x08,umask=0x01/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-st-tlb-tw-pki": ["cpu/event=0x49,umask=0x01/", "cpu/event=0xc0,umask=0x0/", 1000],
}
ICX_CTRS = {
    "stall_frontend_pkc": ["cpu/event=0x9C,umask=0x1,cmask=0x5/", "cpu/event=0x3c,umask=0x0/", 1000],
    "stall_backend_pkc": ["cpu/event=0xa4,umask=0x2/", "cpu/event=0xa4,umask=0x01/", 1000], 
}
SPR_CTRS = {
    "l2-mpki": ["cpu/event=0x25,umask=0x1f/", "cpu/event=0xc0,umask=0x0/", 1000],
    "inst-tlb-mpki": ["cpu/event=0x11,umask=0x20/", "cpu/event=0xc0,umask=0x0/", 1000],
    "inst-tlb-tw-pki": ["cpu/event=0x11,umask=0x0e/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-rd-tlb-mpki": ["cpu/event=0x12,umask=0x20/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-st-tlb-mpki": ["cpu/event=0x13,umask=0x20/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-rd-tlb-tw-pki": ["cpu/event=0x12,umask=0x0e/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-st-tlb-tw-pki": ["cpu/event=0x13,umask=0x0e/", "cpu/event=0xc0,umask=0x0/", 1000],
    "stall_frontend_pkc": ["cpu/event=0x9c,umask=0x1,cmask=0x6/", "cpu/event=0x3c,umask=0x0/", 1000],
    "stall_backend_pkc": ["cpu/event=0xa4,umask=0x2/", "cpu/event=0xa4,umask=0x01/", 1000],
}
UNIVERSAL_AMD_CTRS = {
    "ipc": ["cpu/event=0xc0,umask=0x0/", "cpu/event=0x76,umask=0x0/", 1],
    "branch-mpki": ["cpu/event=0xc3,umask=0x0/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-l1-mpki": ["cpu/event=0x44,umask=0xff/", "cpu/event=0xc0,umask=0x0/", 1000],
    "inst-l1-mpki": ["cpu/event=0x60,umask=0x10/", "cpu/event=0xc0,umask=0x0/", 1000],
    "l2-mpki": ["cpu/event=0x64,umask=0x9/", "cpu/event=0xc0,umask=0x0/", 1000],
    "l3-mpki": ["cpu/event=0x44,umask=0x8/", "cpu/event=0xc0,umask=0x0/", 1000],
    "stall_frontend_pkc": ["cpu/event=0xa9,umask=0x0/", "cpu/event=0x76,umask=0x0/", 1000],
    "inst-tlb-mpki": ["cpu/event=0x84,umask=0x0/", "cpu/event=0xc0,umask=0x0/", 1000],
    "inst-tlb-tw-pki": ["cpu/event=0x85,umask=0x0f/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-tlb-mpki": ["cpu/event=0x45,umask=0xff/", "cpu/event=0xc0,umask=0x0/", 1000],
    "data-tlb-tw-pki": ["cpu/event=0x45,umask=0xf0/", "cpu/event=0xc0,umask=0x0/", 1000],
}
MILAN_CTRS = {
    "stall_backend_pkc1": ["cpu/event=0xae,umask=0xf7/", "cpu/event=0x76,umask=0x0/", 1000],
    "stall_backend_pkc2": ["cpu/event=0xaf,umask=0x27/", "cpu/event=0x76,umask=0x0/", 1000],
}
GENOA_CTRS = {
    "stall_backend_pkc": ["cpu/event=0x1a0,umask=0x1e/", "cpu/event=0x76,umask=0x0/", 1000 * (1.0 / 6.0)]
}

filter_proc = {
    "Graviton2": UNIVERSAL_GRAVITON_CTRS,
    "Graviton3": {**UNIVERSAL_GRAVITON_CTRS, **GRAVITON3_CTRS},
    "Graviton4": {**UNIVERSAL_GRAVITON_CTRS, **GRAVITON3_CTRS},
    "Intel(R) Xeon(R) Platinum 8124M CPU @ 3.00GHz": UNIVERSAL_INTEL_CTRS,
    "Intel(R) Xeon(R) Platinum 8175M CPU @ 2.50GHz": UNIVERSAL_INTEL_CTRS,
    "Intel(R) Xeon(R) Platinum 8275CL CPU @ 3.00GHz": UNIVERSAL_INTEL_CTRS,
    "Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz": UNIVERSAL_INTEL_CTRS,
    "Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz": {**UNIVERSAL_INTEL_CTRS, **ICX_CTRS},
    "Intel(R) Xeon(R) Platinum 8488C": {**UNIVERSAL_INTEL_CTRS, **SPR_CTRS},
    "Milan": {**UNIVERSAL_AMD_CTRS, **MILAN_CTRS},
    "Genoa": {**UNIVERSAL_AMD_CTRS, **GENOA_CTRS},
}

if __name__ == "__main__":
    processor_version = get_cpu_type()
    try:
        stat_choices = list(filter_proc[processor_version].keys())
    except Exception:
        print(f"{processor_version} is not supported")
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--stat", default="ipc", type=str, choices=stat_choices)
    parser.add_argument("--period", default=1000, type=int)
    parser.add_argument("--cpu-list", action="store", type=str)
    parser.add_argument("--no-plot", action="store_true", help="Do not plot to terminal")
    parser.add_argument("--log-file", help="Save counter data as CSV to specified file")
    parser.add_argument("--time", default=60, type=int, help="How long to measure for in seconds")
    parser.add_argument("--custom_ctr", type=str,
                        help="Specify a custom counter ratio and scaling factor as 'name|ctr1|ctr2|scale'"
                             ", calculated as ctr1/ctr2 * scale")
    parser.add_argument("--no-root", action="store_true", help="Allow running without root privileges")

    args = parser.parse_args()

    if not args.no_root:
        res = subprocess.run(["id", "-u"], check=True, stdout=subprocess.PIPE)
        if int(res.stdout) > 0:
            print("Must be run with root privileges (or with --no-root)")
            exit(1)

    if args.custom_ctr:
        ctrs = args.custom_ctr.split("|")
        counter_info = [ctrs[1], ctrs[2], int(ctrs[3])]
        # Override the name of the stat to a user defined name
        stat_name = ctrs[0]
    else:
        counter_info = filter_proc[processor_version][args.stat]
        stat_name = args.stat

    cpus = None
    if args.cpu_list and args.cpu_list != "all":
        cpus = args.cpu_list.split(",")
    csv = perfstat(args.time, args.period, cpus, *counter_info)
    plot_counter_stat(csv, args.log_file, (not args.no_plot), stat_name, *counter_info)
