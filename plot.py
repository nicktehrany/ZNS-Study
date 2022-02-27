from plot.IO_Perf import * 
import os
import glob
import json


def parse_fio_data(file_path, bw_data):
    if os.listdir(f'{file_path}/IO_Performance/data/bandwidth') == []: 
        print("No data in directory")
        exit

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
            bw_data[file]=dict()
            bw_data[file] = json.load(temp)
            os.remove(os.path.join(os.getcwd(), "temp.json"))

if __name__ == "__main__":
    bw_data=dict()
    zone_data=dict()
    queue_depths=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    os.makedirs(f"{file_path}/figures", exist_ok=True)

    parse_fio_data(file_path, bw_data)
    plot_IO_Perf_bw(file_path, bw_data, queue_depths)
    plot_IO_Perf_lat(file_path, bw_data, queue_depths)
