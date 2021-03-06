#! /usr/bin/python3

import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.patches as mpatches

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize

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

def plot_IO_Perf_bw(file_path, data, block_sizes):
    bw_write = [None] * len(block_sizes)
    bw_randwrite = [None] * len(block_sizes)
    bw_read = [None] * len(block_sizes)
    bw_randread = [None] * len(block_sizes)
    bw_overwrite = [None] * len(block_sizes)
    bw_overwrite_rand = [None] * len(block_sizes)

    for key, value in data.items():
        if '_write_' in key:
        # -12 as we are starting at 4K = 2^12 and map that to array index 0 and [:-2] to drop the K from 4K bs and multiply by 1024 for K value
            bw_write[int(math.log2(int(value["jobs"][0]["job options"]["bs"][:-2])*1024)) - 12] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif '_randwrite_' in key:
            bw_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["bs"][:-2])*1024)) - 12] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif '_read_' in key:
            bw_read[int(math.log2(int(value["jobs"][0]["job options"]["bs"][:-2])*1024)) - 12] = value["jobs"][0]["read"]["bw_mean"]/1024
        elif '_randread_' in key:
            bw_randread[int(math.log2(int(value["jobs"][0]["job options"]["bs"][:-2])*1024)) - 12] = value["jobs"][0]["read"]["bw_mean"]/1024
        elif '_overwrite-seq_' in key:
            bw_overwrite[int(math.log2(int(value["jobs"][0]["job options"]["bs"][:-2])*1024)) - 12] = value["jobs"][0]["write"]["bw_mean"]/1024
        elif '_overwrite-rand_' in key:
            bw_overwrite_rand[int(math.log2(int(value["jobs"][0]["job options"]["bs"][:-2])*1024)) - 12] = value["jobs"][0]["write"]["bw_mean"]/1024

    fig, ax = plt.subplots()

    xticks=np.arange(0,6,1)
    ax.plot(xticks, bw_write, markersize=4, marker='x', label="write_seq")
    ax.plot(xticks, bw_randwrite, markersize=4, marker='o', label="write_rand")
    ax.plot(xticks, bw_read, markersize=4, marker='v', label="read_seq")
    ax.plot(xticks, bw_randread, markersize=4, marker='^', label="read_rand")
    ax.plot(xticks, bw_overwrite, markersize=4, marker='<', label="overwrite_seq")
    ax.plot(xticks, bw_overwrite_rand, markersize=4, marker='>', label="overwrite_rand")
    
    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best')
    ax.xaxis.set_ticks(xticks)
    block_labels = [x[:-2] for x in block_sizes]
    ax.xaxis.set_ticklabels(block_labels)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Bandwidth (MiB/sec)")
    ax.set_xlabel("Block Size (KiB)")
    plt.savefig(f"{file_path}/scaled_bandwidth.pdf", bbox_inches="tight")
    plt.clf()
    fig = ax = None

def plot_IO_Perf_concur_write_lat(file_path, data, numjobs, type):
    median_deadline = [None] * len(numjobs)
    tail_deadline = [None] * len(numjobs)
    median_none = [None] * len(numjobs)
    tail_none = [None] * len(numjobs)
    if type == 'iodepth':
        tail = "95.000000"
    else:
        tail = "95.000000"

    for key, value in data.items():
        if '_mq-deadline_' in key and type != 'iodepth':
            median_deadline[int(value["jobs"][0]["job options"]["numjobs"]) - 1] = value["jobs"][0]["write"]["clat_ns"]["percentile"]["50.000000"]/1000
            tail_deadline[int(value["jobs"][0]["job options"]["numjobs"]) - 1] = value["jobs"][0]["write"]["clat_ns"]["percentile"][tail]/1000
        elif '_mq-deadline_' in key and type == 'iodepth':
            median_deadline[int(value["jobs"][0]["job options"]["iodepth"]) - 1] = value["jobs"][0]["write"]["clat_ns"]["percentile"]["50.000000"]/1000
            tail_deadline[int(value["jobs"][0]["job options"]["iodepth"]) - 1] = value["jobs"][0]["write"]["clat_ns"]["percentile"][tail]/1000
        elif '_none_' in key:
            median_none[int(value["jobs"][0]["job options"]["numjobs"]) - 1] = value["jobs"][0]["write"]["clat_ns"]["percentile"]["50.000000"]/1000
            tail_none[int(value["jobs"][0]["job options"]["numjobs"]) - 1] = value["jobs"][0]["write"]["clat_ns"]["percentile"][tail]/1000

    fig, ax = plt.subplots()

    ax.plot(numjobs, median_deadline, markersize=6, marker='x', color="orange")
    ax.plot(numjobs, tail_deadline, markersize=6, marker='o', color="orange")
    ax.plot(numjobs, median_none, markersize=6, marker='x', color="green")
    ax.plot(numjobs, tail_none, markersize=6, marker='o', color="green")

    # Creating the legend labels
    handles = []
    handles.append(mpatches.Patch(color="orange", label="mq-deadline"))
    handles.append(mpatches.Patch(color="green", label="none"))
    handles.append(plt.Line2D([], [], color="black", marker="x", label="median", linewidth=0))
    handles.append(plt.Line2D([], [], color="black", marker="o", label=f"95%", linewidth=0))

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best', handles=handles)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Latency (usec)")
    ax.set_xlabel("Number of Outstanding I/Os")
    if type == "seq":
        plt.savefig(f"{file_path}/concur_write_seq.pdf", bbox_inches="tight")
    else:
        plt.savefig(f"{file_path}/concur_write_seq_iodepth.pdf", bbox_inches="tight")
    plt.clf()

def plot_IO_Perf_concur_read_lat(file_path, data, numjobs, type):
    median_deadline = [None] * len(numjobs)
    tail_deadline = [None] * len(numjobs)
    median_none = [None] * len(numjobs)
    tail_none = [None] * len(numjobs)

    for key, value in data.items():
        if '_none_' in key and not 'iodepth' in type:
            index = int(value["jobs"][0]["job options"]["numjobs"]) - 1
        elif 'iodepth' in type:
            index = int(value["jobs"][0]["job options"]["iodepth"]) - 1
        elif '_mq-deadline_' in type:
            index = int(value["jobs"][0]["job options"]["numjobs"]) - 1
        else:
            index = int(value["jobs"][0]["job options"]["iodepth"]) - 1

        if '_mq-deadline_' in key:
            median_deadline[index] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["50.000000"]/1000
            tail_deadline[index] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["95.000000"]/1000
        elif '_none_' in key and type == 'seq_iodepth':
            median_none[index] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["50.000000"]/1000
            tail_none[index] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["95.000000"]/1000
        elif '_none_' in key:
            median_none[index] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["50.000000"]/1000
            tail_none[index] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["95.000000"]/1000

    fig, ax = plt.subplots()

    ax.plot(numjobs, median_deadline, markersize=6, marker='x', color="orange")
    ax.plot(numjobs, tail_deadline, markersize=6, marker='o', color="orange")
    ax.plot(numjobs, median_none, markersize=6, marker='x', color="green")
    ax.plot(numjobs, tail_none, markersize=6, marker='o', color="green")

    # Creating the legend labels
    handles = []
    handles.append(mpatches.Patch(color="orange", label="mq-deadline"))
    handles.append(mpatches.Patch(color="green", label="none"))
    handles.append(plt.Line2D([], [], color="black", marker="x", label="median", linewidth=0))
    handles.append(plt.Line2D([], [], color="black", marker="o", label="95%", linewidth=0))

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best', handles=handles)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Latency (usec)")
    if 'iodepth' in type:
        ax.set_xlabel("I/O Queue Depth")
    else:
        ax.set_xlabel("Number of Outstanding I/Os")
    plt.savefig(f"{file_path}/concur_read_{type}.pdf", bbox_inches="tight")
    plt.clf()
