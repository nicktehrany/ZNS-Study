#! /usr/bin/python3

import matplotlib.pyplot as plt
import os
import glob
import json
import math
import numpy as np
import matplotlib.patches as mpatches

bw_data=dict()
zone_data=dict()
file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])
datadir=f"{file_path}/data"
queue_depths=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

def parse_bw_data():
    if os.listdir(f'{datadir}/bandwidth') == []: 
        print("No data in directory")
        exit

    for file in glob.glob(f'{datadir}/bandwidth/*'): 
        with open(file, 'r') as f:
            for index, line in enumerate(f, 1):
                # Removing all fio logs in json file by finding first {
                if line.split()[0] == "{":
                    rows = f.readlines()
                    with open(os.path.join(os.getcwd(), "temp.json"), 'w+') as temp:
                        temp.write(line)
                        temp.writelines(rows)
                    break
        with open(os.path.join(os.getcwd(), "temp.json"), 'r') as temp:
            bw_data[file]=dict()
            bw_data[file] = json.load(temp)
            os.remove(os.path.join(os.getcwd(), "temp.json"))

def plot_bw():
    bw_write = [None] * len(queue_depths)
    bw_randwrite = [None] * len(queue_depths)
    bw_read = [None] * len(queue_depths)
    bw_randread = [None] * len(queue_depths)
    bw_overwrite = [None] * len(queue_depths)
    bw_overwrite_rand = [None] * len(queue_depths)

    for key, value in bw_data.items():
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
    ax.set_ylabel("Bandwidth (MiB/s)")
    ax.set_xlabel("I/O Queue Depth")
    os.makedirs(f"{file_path}/figures", exist_ok=True)
    plt.savefig(f"{file_path}/figures/bandwidth.pdf", bbox_inches="tight")
    # plt.show()
    plt.clf()
    fig = ax = None

def plot_lat():
    median_randwrite = [None] * len(queue_depths)
    randwrite_iops = [None] * len(queue_depths)
    tail_randwrite = [None] * len(queue_depths)
    median_randread = [None] * len(queue_depths)
    randread_iops = [None] * len(queue_depths)
    tail_randread = [None] * len(queue_depths)

    for key, value in bw_data.items():
        if '_randwrite_' in key:
            median_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["clat_ns"]["mean"]/1000
            randwrite_iops[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["iops"]
            tail_randwrite[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["write"]["clat_ns"]["percentile"]["95.000000"]/1000
        if '_randread_' in key:
            median_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["clat_ns"]["mean"]/1000
            randread_iops[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["iops"]
            tail_randread[int(math.log2(int(value["jobs"][0]["job options"]["iodepth"])))] = value["jobs"][0]["read"]["clat_ns"]["percentile"]["95.000000"]/1000

    fig, ax = plt.subplots()

    ax.plot(randwrite_iops, median_randwrite, markersize=8, marker='x', color="orange")
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
    # ax.xaxis.set_ticks(np.arange(0,11,1))
    # ax.xaxis.set_ticklabels(queue_depths)
    ax.set_ylabel("Latency (usec)")
    ax.set_xlabel("IOPs")
    os.makedirs(f"{file_path}/figures", exist_ok=True)
    plt.savefig(f"{file_path}/figures/loaded_latency.pdf", bbox_inches="tight")
    # plt.show()
    plt.clf()

if __name__ == "__main__":
    parse_bw_data()
    plot_bw()
    plot_lat()
