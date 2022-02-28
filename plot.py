from plot.IO_Perf import * 
import os
import glob
import json

def parse_fio_data(data_path, data):
    if not os.path.exists(f'{file_path}/IO_Performance/data/{data_path}') or \
        os.listdir(f'{file_path}/IO_Performance/data/{data_path}') == []: 
        print(f"No data in {file_path}/IO_Performance/data/{data_path}")
        return 0 

    for file in glob.glob(f'{file_path}/IO_Performance/data/bandwidth/*'): 
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

if __name__ == "__main__":
    bw_data = dict()
    zone_data = dict()
    queue_depths = 2 ** np.arange(11)
    zones = np.arange(1, 15, 1)
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    os.makedirs(f"{file_path}/figures", exist_ok=True)

    if(parse_fio_data("bandwidth", bw_data)):
        plot_IO_Perf_bw(file_path, bw_data, queue_depths)
        plot_IO_Perf_lat(file_path, bw_data, queue_depths)

    if(parse_fio_data("active_zones", zone_data)):
        plot_IO_Perf_act_zones(file_path, zone_data, zones)
