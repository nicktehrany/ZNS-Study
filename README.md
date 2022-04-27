# ZNS-Study

This repository contains all running scripts for the benchmarks run in the evaluation of NVMe ZNS devices. It additionally contains plotting scripts, as well as collected data and figures. The final paper of this evaluation is also present in this repository [here](Towards_an_Unwritten_Contract_of_NVMe_ZNS_SSD.pdf)

Requirements:

- Linux Kernel 5.9+ (for ZNS support)
- [libnvme](https://github.com/linux-nvme/libnvme)
- [nvme-cli](https://github.com/linux-nvme/nvme-cli)
- [blkzone](https://github.com/util-linux/util-linux)
- [libzbd](https://github.com/westerndigitalcorporation/libzbd)
- [fio](https://github.com/axboe/fio) compiled against libzbd
- [RocksDB](https://github.com/facebook/rocksdb)
- [ZenFS](https://github.com/westerndigitalcorporation/zenfs)
- [f2fs](https://git.kernel.org/pub/scm/linux/kernel/git/jaegeuk/f2fs-tools.git)

## Setup

For the experiments we utilize different devices, however all have the same setup. Namely, we utilize only a subset of the available space (100GB or 50 zones on the ZNS device) and fill the remaining space with cold data. For detailed setup instructions see the [TODO paper](). Note, when filling the ZNS device with cold data, the benchmark needs to have a block size that is a multiple of the zone capacity, such that it can precisely fill a zone and move to the next, filling the entire namespaces. If it is not a multiple, it will continuously reset and rewrite the first zone of the namespace.

```bash
# Create a 100GiB namespace, size is given in 512B sectors
$ sudo nvme create-ns /dev/nvme2 -s 209715200 -c 209715200 -b 512 --csi=2
# Repeat for all namespaces with according size
# Attach all namespaces to same controller (adapt -n argument with ns id)
sudo nvme attach-ns /dev/nvme2 -n 1 -c 0

# Set the correct scheduler for all zoned namespaces (adapt device path for each ns)
$ echo mq-deadline | sudo tee /sys/block/nvme2n2/queue/scheduler

# Fill ZNS free space with cold data
$ sudo fio --name=zns-fio --filename=/dev/nvme2n3 --direct=1 --size=$((4194304*512*`cat /sys/block/nvme2n3/queue/nr_zones`)) --ioengine=libaio --zonemode=zbd --iodepth=8 --rw=write --bs=512K

# Fill conventional SSD free space with cold data
$ sudo fio --name=zns-fio --filename=/dev/nvme0np2 --direct=1 --size=2T --ioengine=libaio --iodepth=8 --rw=write --bs=512K
```

This already sets the mq-deadline scheduler, some of the experiments that benchmark different schedulers will change them.

## Benchmarks

We provide a number of benchmarks that we were using for our evaluation.

- [Block Level I/O Performance](IO_Performance) contains the block level I/O performance benchmarks. For a detailed list of benchmarks see the [README](IO_Performance/README.md) in its directory.

To run the benchmarks:

```bash
$ sudo ./run_benchs nvme2n2
```

It requires the device to be benchmarked (and its namespace) to be specified and then allows selecting the specific benchmark. All collected data will be placed in the respective benchmark directory additionally indicating the device and time, in case experiments are repeated multiple times.

**NOTE** the benchmarks will format namespaces in between runs, hence all data in the namespace will be lost. Therefore, make sure the correct device is specified.

We additionally provide a script to retrieve information of a ZNS device in the [`get_zoned_device_info` script](get_zoned_device_info), which can be run independently to see the characteristics of the device. Run it as `sudo ./get_zoned_device_info nvme2n2` with the ZNS device and namespace indicated.

## Plotting

Running `python3 plot.py` in the root directory of this repo will create plots for all data that exists in the repo. These will appear in the `figures` directory under the respective benchmark and device names.

## Our Configuration

From the existing data we have three devices:

- `nvme0n1p1`, which is a 100GB parition on a Samsung EVO 2TB SSD
- `nvme1n1p2`, which is a 100GB partition on an Optane SSD
- `nvme2n2`, which is a 50 zone (100GB size, ~51GB capacity) namespace on a NVMe ZNS SSD

The conventional SSDs only support a single namespace, hence here we utilize partitions, whereas the ZNS device supports multiple namespaces.
