#! /usr/bin/python3

import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.patches as mpatches

def plot_IO_Perf_bw(file_path, data, queue_depths):
    bw_write = [None] * len(queue_depths)
    bw_randwrite = [None] * len(queue_depths)
    bw_read = [None] * len(queue_depths)
    bw_randread = [None] * len(queue_depths)
    bw_overwrite = [None] * len(queue_depths)
    bw_overwrite_rand = [None] * len(queue_depths)

    for key, value in data.items():
        if '_write_' in key:
            bw_write[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif '_randwrite_' in key:
            bw_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif '_read_' in key:
            bw_read[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["bw_mean"]/1024
        elif '_randread_' in key:
            bw_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["bw_mean"]/1024
        elif '_overwrite-seq_' in key:
            bw_overwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif '_overwrite-rand_' in key:
            bw_overwrite_rand[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["bw_mean"]/1024

    fig, ax = plt.subplots()

    xticks=np.arange(0,11,1)
    ax.plot(xticks, bw_write, markersize=4, marker='x', label="write")
    ax.plot(xticks, bw_randwrite, markersize=4, marker='o', label="randwrite")
    ax.plot(xticks, bw_read, markersize=4, marker='v', label="read")
    ax.plot(xticks, bw_randread, markersize=4, marker='^', label="randread")
    ax.plot(xticks, bw_overwrite, markersize=4, marker='<', label="overwrite_seq")
    ax.plot(xticks, bw_overwrite_rand, markersize=4, marker='>', label="overwrite_rand")
    
    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best')
    ax.xaxis.set_ticks(np.arange(0,11,1))
    ax.xaxis.set_ticklabels(queue_depths)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Bandwidth (MiB/s)")
    ax.set_xlabel("I/O Queue Depth")
    plt.savefig(f"{file_path}/bandwidth.pdf", bbox_inches="tight")
    plt.clf()
    fig = ax = None

def plot_IO_Perf_lat(file_path, data, queue_depths):
    median_randwrite = [None] * len(queue_depths)
    randwrite_iops = [None] * len(queue_depths)
    tail_randwrite = [None] * len(queue_depths)
    median_randread = [None] * len(queue_depths)
    randread_iops = [None] * len(queue_depths)
    tail_randread = [None] * len(queue_depths)

    for key, value in data.items():
        if '_randwrite_' in key:
            median_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["clat_ns"]["mean"]/1000
            randwrite_iops[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops"]
            tail_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["clat_ns"]["percentile"]["95.000000"]/1000
        elif '_randread_' in key:
            median_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["clat_ns"]["mean"]/1000
            randread_iops[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops"]
            tail_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["95.000000"]/1000

    fig, ax = plt.subplots()

    ax.plot(randwrite_iops, median_randwrite, markersize=6, marker='x', color="orange")
    ax.plot(randwrite_iops, tail_randwrite, markersize=6, marker='o', color="orange")
    ax.plot(randread_iops, median_randread, markersize=6, marker='x', color="green")
    ax.plot(randread_iops, tail_randread, markersize=6, marker='o', color="green")

    # Creating the legend labels
    handles = []
    handles.append(mpatches.Patch(color="orange", label="randwrite"))
    handles.append(mpatches.Patch(color="green", label="randread"))
    handles.append(plt.Line2D([], [], color="black", marker="x", label="median"))
    handles.append(plt.Line2D([], [], color="black", marker="o", label="95%"))

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best', handles=handles)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Latency (usec)")
    ax.set_xlabel("IOPs")
    plt.savefig(f"{file_path}/loaded_latency.pdf", bbox_inches="tight")
    plt.clf()

def plot_IO_Perf_act_zones(file_path, data, zones):
    bw_randwrite = [None] * len(zones)
    bw_randread = [None] * len(zones)
    bw_randoverwrite = [None] * len(zones)

    for key, value in data.items():
        if '_randwrite_' in key:
            bw_randwrite[int(value["jobs"][0]["job options"]["max_open_zones"]) - 1] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif 'randread_' in key:
            bw_randread[int(value["jobs"][0]["job options"]["max_open_zones"]) - 1] = value["jobs"][0]["read"]["bw_mean"]/1024
        elif '_randoverwrite_' in key:
            bw_randoverwrite[int(value["jobs"][0]["job options"]["max_open_zones"]) - 1] = value["jobs"][0]["write"]["bw_mean"]/1024

    fig, ax = plt.subplots()

    ax.plot(zones, bw_randwrite, markersize=6, marker='x', label="randwrite")
    ax.plot(zones, bw_randread, markersize=6, marker='o', label="randread")
    ax.plot(zones, bw_randoverwrite, markersize=6, marker='v', label="overwrite_rand")

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Bandwidth (MiB/s)")
    ax.set_xlabel("Active Zones")
    plt.savefig(f"{file_path}/active_zones.pdf", bbox_inches="tight")
    plt.clf()
