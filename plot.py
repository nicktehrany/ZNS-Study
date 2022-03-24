from plot.IO_Perf import * 
import os
import glob
import json

def parse_fio_data(data_path, data):
    if not os.path.exists(f'{data_path}') or \
            os.listdir(f'{data_path}') == []: 
        print(f"No data in {data_path}")
        return 0 

    for file in glob.glob(f'{data_path}/*'): 
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
            data[file] = dict()
            data[file] = json.load(temp)
            os.remove(os.path.join(os.getcwd(), "temp.json"))

    return 1

def prep_IO_Perf(file_path):
    bw_data = dict()
    zone_data = dict()
    scaled_bw_data = dict()
    concur_write_data = dict()
    concur_read_data = dict()
    queue_depths = 2 ** np.arange(11)
    block_sizes = ["4Ki", "8Ki", "16Ki", "32Ki", "64Ki", "128Ki"]
    zones = np.arange(1, 15, 1)
    numjobs = np.arange(1, 15, 1)

    for dir in glob.glob(f'{file_path}/IO_Performance/data/throughput/*'): 
        dir = dir.split('/')[-1]
        os.makedirs(f"{file_path}/figures/IO_Perf/{dir}", exist_ok=True)

        if(parse_fio_data(f'{file_path}/IO_Performance/data/throughput/{dir}', bw_data)):
            plot_IO_Perf_iops(f'{file_path}/figures/IO_Perf/{dir}', bw_data, queue_depths)
            plot_IO_Perf_lat(f'{file_path}/figures/IO_Perf/{dir}', bw_data, queue_depths)

    for dir in glob.glob(f'{file_path}/IO_Performance/data/active_zones/*'): 
        dir = dir.split('/')[-1]
        os.makedirs(f"{file_path}/figures/IO_Perf/{dir}", exist_ok=True)

        if(parse_fio_data(f'{file_path}/IO_Performance/data/active_zones/{dir}', zone_data)):
            plot_IO_Perf_act_zones(f'{file_path}/figures/IO_Perf/{dir}', zone_data, zones)

    for dir in glob.glob(f'{file_path}/IO_Performance/data/scaled_bandwidth/*'): 
        dir = dir.split('/')[-1]
        os.makedirs(f"{file_path}/figures/IO_Perf/{dir}", exist_ok=True)

        if(parse_fio_data(f'{file_path}/IO_Performance/data/scaled_bandwidth/{dir}', scaled_bw_data)):
            plot_IO_Perf_bw(f'{file_path}/figures/IO_Perf/{dir}', scaled_bw_data, block_sizes)

    for dir in glob.glob(f'{file_path}/IO_Performance/data/concur_write_seq/*'): 
        dir = dir.split('/')[-1]
        os.makedirs(f"{file_path}/figures/IO_Perf/{dir}", exist_ok=True)

        if(parse_fio_data(f'{file_path}/IO_Performance/data/concur_write_seq/{dir}', concur_write_data)):
            plot_IO_Perf_concur_write_lat(f'{file_path}/figures/IO_Perf/{dir}', concur_write_data, numjobs)

    for dir in glob.glob(f'{file_path}/IO_Performance/data/concur_read_seq/*'): 
        dir = dir.split('/')[-1]
        os.makedirs(f"{file_path}/figures/IO_Perf/{dir}", exist_ok=True)

        if(parse_fio_data(f'{file_path}/IO_Performance/data/concur_read_seq/{dir}', concur_read_data)):
            plot_IO_Perf_concur_read_lat(f'{file_path}/figures/IO_Perf/{dir}', concur_read_data, numjobs)

if __name__ == "__main__":
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    prep_IO_Perf(file_path)
