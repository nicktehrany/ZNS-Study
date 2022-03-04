#! /usr/bin/python3

import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.patches as mpatches

def plot_IO_Perf_iops(file_path, data, queue_depths):
    iops_write = [None] * len(queue_depths)
    iops_write_stdev = [None] * len(queue_depths)
    iops_randwrite = [None] * len(queue_depths)
    iops_randwrite_stdev = [None] * len(queue_depths)
    iops_read = [None] * len(queue_depths)
    iops_read_stdev = [None] * len(queue_depths)
    iops_randread = [None] * len(queue_depths)
    iops_randread_stdev = [None] * len(queue_depths)
    iops_overwrite = [None] * len(queue_depths)
    iops_overwrite_stdev = [None] * len(queue_depths)
    iops_overwrite_rand = [None] * len(queue_depths)
    iops_overwrite_rand_stdev = [None] * len(queue_depths)

    for key, value in data.items():
        if '_write_' in key:
            iops_write[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_mean"]/1000
            iops_write_stdev[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_stddev"]/1000
        elif '_randwrite_' in key:
            iops_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_mean"]/1000
            iops_randwrite_stdev[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_stddev"]/1000
        elif '_read_' in key:
            iops_read[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops_mean"]/1000
            iops_read_stdev[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops_stddev"]/1000
        elif '_randread_' in key:
            iops_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops_mean"]/1000
            iops_randread_stdev[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops_stddev"]/1000
        elif '_overwrite-seq_' in key:
            iops_overwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_mean"]/1000
            iops_overwrite_stdev[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_stddev"]/1000
        elif '_overwrite-rand_' in key:
            iops_overwrite_rand[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_mean"]/1000
            iops_overwrite_rand_stdev[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_stddev"]/1000

    fig, ax = plt.subplots()

    xticks=np.arange(0,11,1)
    ax.plot(xticks, iops_write, markersize=4, marker='x', label="write_seq")
    ax.plot(xticks, iops_randwrite, markersize=4, marker='o', label="write_rand")
    ax.plot(xticks, iops_read, markersize=4, marker='v', label="read_seq")
    ax.plot(xticks, iops_randread, markersize=4, marker='^', label="read_rand")
    ax.plot(xticks, iops_overwrite, markersize=4, marker='<', label="overwrite_seq")
    ax.plot(xticks, iops_overwrite_rand, markersize=4, marker='>', label="overwrite_rand")
    
    # With error bars
    # ax.errorbar(xticks, iops_write, yerr=iops_write_stdev, markersize=4, capsize=3, marker='x', label="write_seq")
    # ax.errorbar(xticks, iops_randwrite, yerr=iops_randwrite_stdev, markersize=4, capsize=3, marker='o', label="write_rand")
    # ax.errorbar(xticks, iops_read, yerr=iops_read_stdev, markersize=4, capsize=3, marker='v', label="read_seq")
    # ax.errorbar(xticks, iops_randread, yerr=iops_randread_stdev, markersize=4, capsize=3, marker='^', label="read_rand")
    # ax.errorbar(xticks, iops_overwrite, yerr=iops_overwrite_stdev, markersize=4, capsize=3, marker='<', label="overwrite_seq")
    # ax.errorbar(xticks, iops_overwrite_rand, yerr=iops_overwrite_rand_stdev, markersize=4, capsize=3, marker='>', label="overwrite_rand")
    
    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best')
    ax.xaxis.set_ticks(np.arange(0,11,1))
    ax.xaxis.set_ticklabels(queue_depths)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Throughput (x1000 IOPs/sec)")
    ax.set_xlabel("I/O Queue Depth")
    plt.savefig(f"{file_path}/throughput.pdf", bbox_inches="tight")
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
            randwrite_iops[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops_mean"]/1000
            tail_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["clat_ns"]["percentile"]["95.000000"]/1000
        elif '_randread_' in key:
            median_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["clat_ns"]["mean"]/1000
            randread_iops[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops_mean"]/1000
            tail_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["95.000000"]/1000

    fig, ax = plt.subplots()

    ax.plot(randwrite_iops, median_randwrite, markersize=6, marker='x', label="median")
    ax.plot(randwrite_iops, tail_randwrite, markersize=6, marker='o', label="95%")
    # ax.plot(randread_iops, median_randwrite, markersize=6, marker='x', label="median")
    # ax.plot(randread_iops, tail_randwrite, markersize=6, marker='o', label="95%")

    # Commented out part for randwrite and randread in same plot
    # ax.plot(randwrite_iops, median_randwrite, markersize=6, marker='x', color="orange")
    # ax.plot(randwrite_iops, tail_randwrite, markersize=6, marker='o', color="orange")
    # ax.plot(randread_iops, median_randread, markersize=6, marker='x', color="green")
    # ax.plot(randread_iops, tail_randread, markersize=6, marker='o', color="green")

    # Creating the legend labels
    # handles = []
    # handles.append(mpatches.Patch(color="orange", label="write_rand"))
    # handles.append(mpatches.Patch(color="green", label="read_rand"))
    # handles.append(plt.Line2D([], [], color="black", marker="x", label="median"))
    # handles.append(plt.Line2D([], [], color="black", marker="o", label="95%"))

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    # ax.legend(loc='best', handles=handles)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Latency (usec)")
    ax.set_xlabel("Throughput (x1000 IOPs/sec)")
    plt.savefig(f"{file_path}/loaded_latency.pdf", bbox_inches="tight")
    plt.clf()

def plot_IO_Perf_act_zones(file_path, data, zones):
    iops_randwrite = [None] * len(zones)
    iops_randread = [None] * len(zones)
    iops_randoverwrite = [None] * len(zones)

    for key, value in data.items():
        if '_randwrite_' in key:
            iops_randwrite[int(value["jobs"][0]["job options"]["max_open_zones"]) - 1] = value["jobs"][0]["write"]["iops_mean"]/1000
        elif 'randread_' in key:
            iops_randread[int(value["jobs"][0]["job options"]["max_open_zones"]) - 1] = value["jobs"][0]["read"]["iops_mean"]/1000
        elif '_randoverwrite_' in key:
            iops_randoverwrite[int(value["jobs"][0]["job options"]["max_open_zones"]) - 1] = value["jobs"][0]["write"]["iops_mean"]/1000

    fig, ax = plt.subplots()

    ax.plot(zones, iops_randwrite, markersize=6, marker='x', label="write_rand")
    ax.plot(zones, iops_randread, markersize=6, marker='o', label="read_rand")
    ax.plot(zones, iops_randoverwrite, markersize=6, marker='v', label="overwrite_rand")

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best')
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Throughput (x1000 IOPs/sec")
    ax.set_xlabel("Active Zones")
    plt.savefig(f"{file_path}/active_zones.pdf", bbox_inches="tight")
    plt.clf()
