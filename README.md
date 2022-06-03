# ZNS-Study

This repository contains all running scripts for the benchmarks used in the evaluation of NVMe ZNS devices. It
additionally contains plotting scripts, as well as collected datasets and figures. The technical report for this
evaluation is available //TODO: link report once published

This README contains a collection of commands and instructions for setting up of ZNS devices. For a detailed
documentation of ZNS devices also consult the [Official ZNS Documentation](https://zonedstorage.io/docs/introduction).

## Requirements:

ZNS devices and this evaluation requires several libraries and tools to be installed, *Important to note is that ZNS
support is very new in the majority of projects, thus ensure that versions are as new as possible and up to date with
the master branch*

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

Throughout this guide, commands and set up explanation contain names of the specific NVMe device which are depicting
their configuration in our system.

- `nvme0n1p1`, is a 100GB parition on a Samsung EVO 2TB SSD
- `nvme1n1p2`, is a 100GB partition on an Optane SSD
- `nvme2n2`, is a 50 zone (100GB size, ~51GB capacity) namespace on a NVMe ZNS SSD

Note, the conventional SSDs only support a single namespace, hence here we utilize partitions, whereas the ZNS device
supports multiple namespaces.

### How to create namespaces on ZNS devices

The ZNS device used in this evaluation is capable of exposing a small subsets of its available capacity at randomly
writeable space, and the remaining available space can be exposed as zoned storage. For this we can set up different
namespaces for the randomly writable and zoned space, respectively. Each namespace (that is zoned) also requires the
correct scheduler to be set (for detailed scheduling information see the background section in our report and the
[documentation I/O scheduler configuration](https://zonedstorage.io/docs/linux/sched#block-io-scheduler-configuration)).

```bash
# Create a 4GiB conventional namespace, size is given in 512B sectors
sudo nvme create-ns /dev/nvme2 -s 8388608 -c 8388608 -b 512 --csi=0

# Create a 100GiB conventional namespace, note the csi changed to zoned
$ sudo nvme create-ns /dev/nvme2 -s 209715200 -c 209715200 -b 512 --csi=2

# Attach all namespaces to same controller (adapt -n argument with ns id)
sudo nvme attach-ns /dev/nvme2 -n 1 -c 0

# Set the correct scheduler for the zoned namespaces (adapt device path for each ns)
$ echo mq-deadline | sudo tee /sys/block/nvme2n2/queue/scheduler
```

### Getting information about the ZNS namespace

Once the ZNS zoned namespace is created, there a number of properties we can retrieve from it which we require for the
benchmarks we run. For this we have the `get_zoned_device_info` script, which can be run as `sudo
./get_zoned_device_info nvme2n2` to get all ZNS information. However, the commands can additionally be run individually
as follows,

```bash
# Get the available device capacity in 512B sectors
$ sudo nvme id-ctrl /dev/nvme2 | grep tnvmcap | awk '{print $3/512}'

# Get the zone capacity in MiB 
$ sudo nvme zns report-zones /dev/nvme2n2 -d 1 | grep -o 'Cap:.*$' | awk '{print strtonum($2)*512/1024/1024}'

# Get maximum supported active zones
$ cat /sys/block/nvme2n2/queue/max_active_zones

# Get the supported sector sizes in powers of 2
$ sudo nvme id-ns /dev/nvme2n2 | grep -o "lbads:[0-9]*"

# Get NUMA node device is attached at
$ cat/sys/block/nvme2n1/device/numa_node
```

### Formatting and mounting f2fs on ZNS devices

f2fs has support for zoned storage devices added. Using `mkfs.f2fs` (from `f2fs-tools`, make sure its version is at
least equal to 1.14.0) the ZNS zoned namespace can be formatted with the f2fs file system and mounted. However, f2fs
requires an additional regular randomly writable block device for its superblock and write caching. Additionally, both
devices have to be configured to the same sector size (512B in our case).

```bash
# Format devices, one or more zoned devices followed by a single randomly writable block device
$ sudo mkfs.f2fs -f -m -c /dev/nvme2n2 /dev/nvme2n1

# mount the file system with the randomly writable device (where the superblock is)
$ sudo mount -t f2fs /dev/nvme2n1 /mnt/f2fs/
```

### Creating a ZenFS file system 

To run RocksDB on the ZNS device, it requires the ZenFS plugin and a ZenFS file system to be formatted. To format the
file system we specify the zoned namespace to use and an additional auxiliary path for it to place RocksDB LOG and LOCK
files. In the command below we place the auxiliary path on a mounted device with f2fs.

```bash
$ sudo ./plugin/zenfs/util/zenfs mkfs --zbd=nvme2n2 --aux_path=/home/nty/rocksdb_aux_path/zenfs2n2
```

### Namespace initialization

For the experiments we utilize different devices, however all have the same setup. Namely, we utilize only a subset of
the available space (100GB or 50 zones on the ZNS device) and fill the remaining space with cold data. Thus we only
created a 100GiB namespace in the prior ZNS setup commands, for the additional cold data space simply repeat this
process and increase the size to the remaining available space on the device. 

```bash
# Fill ZNS free space with cold data
$ sudo fio --name=zns-fio --filename=/dev/nvme2n3 --direct=1 --size=$((4194304*512*`cat /sys/block/nvme2n3/queue/nr_zones`)) --ioengine=libaio --zonemode=zbd --iodepth=8 --rw=write --bs=512K

# Fill conventional SSD free space with cold data
$ sudo fio --name=zns-fio --filename=/dev/nvme0np2 --direct=1 --size=2T --ioengine=libaio --iodepth=8 --rw=write --bs=512K
```

Note, when filling the ZNS device with cold data, the benchmark needs to have a block size that is a multiple of the
zone capacity, such that it can precisely fill a zone and move to the next, filling the entire namespaces. If it is not
a multiple, it will continuously reset and rewrite the first zone of the namespace.

## Benchmarks

We provide a number of benchmarks that we were using for our evaluation.

- [Block Level I/O Performance](IO_Performance) contains the block level I/O performance benchmarks. For a detailed list
  of benchmarks see the [README](IO_Performance/README.md) in its directory.

To run the benchmarks:

```bash
$ sudo ./run_benchs nvme2n2
```

It requires the device to be benchmarked (and its namespace) to be specified and then allows selecting the specific
benchmark. All collected data will be placed in the respective benchmark directory additionally indicating the device
and time, in case experiments are repeated multiple times.

**NOTE** the benchmarks will format namespaces in between runs, hence all data in the namespace will be lost. Therefore,
make sure the correct device is specified.

## Plotting

Running `python3 plot.py` in the root directory of this repo will create plots for all data that exists in the repo.
These will appear in the `figures` directory under the respective benchmark and device names.
