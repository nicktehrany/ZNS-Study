# Block Level I/O Performance Benchmarks

This directory contains the block level I/O performance benchmarks for the different devices, and their collected data. While not all of the benchmarks were used in the end as some failed to show the intended results, they all remain here. Numerous of the benchmarks were initially thought to be successful however, turned out to be wrong on non-logical setups. We hope the mistakes made here and lessons learned will help others, hence we left the invalid benchmarks and provide explanations on what is invalid below. We have the following benchmarks

## fio_active_zones

This benchmark measures the random write performance with fio on an increasing number of active zones, under block size of `4KiB` and a queue depth of `16`. This benchmark was **not** used as it primarily measures the random write performance, which ZNS devices do not support, and hence it mainly measures fio's implementation of handling random writing to ZNS devices.

## fio_concur_read_rand

This benchmark measures the random read performance of the ZNS device for the `mq-deadline` and `none` schedulers. With `mq-deadline` it increases the iodepth up to 14 with a single active zone (since mq-deadline can hold back I/Os for the device if iodepth is larger than 1), and `none` uses a single iodepth with increasing number of concurrent threads (up to 14), each reading at a 3 zone offset. This benchmark was also **not** used, as it is measuring I/O performance of read, where there are no device constraints, hence even none scheduler could have deep I/O queues.

## fio_concur_read_seq

This benchmark repeats what was done in the prior fio_concur_read_rand benchmark only with sequential reading.

## fio_concur_read_seq_iodepth

This benchmark again compares the `mq-deadline` and `none` schedulers under sequential reading. Here we increase the iodepth for both with a single zone, as there are no read ordering constraints no I/Os need to be held back. We use a block size of `4KiB`.

## fio_concur_write_seq

This benchmark again compared the `mq-deadline` and `none` scheduler with the same command, where both are writing with an iodepth of 1 and block size of `4KiB`, and the number of concurrent threads is increased up to 14. Each thread writes at a 3 zone offset, and writing is sequential.

## fio_concur_write_seq_iodepth

This benchmark compares the `mq-deadline` and `none` schedulers under writing workload. Similarly, we increase the iodepth for mq-deadline on a single zone, as it can hold back write I/Os and now we have a sequential write constraint. And to enforce there is no on-device ordering (see section 3.4.1 of the NVMe 2.0 specification) the scheduler needs to hold I/Os back. The none scheduler does not do this, hence it can only have an iodepth of 1. Therefore, this benchmark increases the number of concurrent threads for none (up to 14, since we have 14 maximum active zones), with each an iodepth of 1.

## fio_scaled_bandwidth

This benchmark runs a number of read/write (random and sequential) benchmark with an increasing block size from `4KiB` up to `128KiB` in powers of 2) with an iodepth of 4. This shows the maximum achievable bandwidth of a device. This benchmark is run on the conventional and ZNS devices.

## fio_throughput

This benchmark similarly uses a block size of `4KiB` however increases the iodepth from `1` to `1024` in powers of 2. Based on this we can retrieve the maximum achievable IOPs for the devices (conventional and ZNS).
