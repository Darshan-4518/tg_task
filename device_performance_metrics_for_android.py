import csv
import os
import sys
import time
import re
from ppadb.client import Client as AdbClient


class DeviceMetricsForAndroid:

    def __init__(self,device_udid,file_path=""):
        self.device_udid = device_udid
        self.is_running = True
        self.file_path = file_path
        self.fieldnames = ["PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "[%CPU]", "%MEM","TIME+","ARGS"]
        with open(file_path+"device_metrics_data.csv",mode="w",newline="") as file:
            writer = csv.DictWriter(file,self.fieldnames)
            writer.writeheader()

    def append_metrics_data(self,rows):
        with open(self.file_path + "data.csv",mode="a",newline="") as file:
           writer = csv.DictWriter(file,self.fieldnames)
           writer.writerows(rows)
           writer.writerow({})

    def start_metrics(self):
        client = AdbClient(host="localhost",port=5037)
        device = client.device(self.device_udid)


        while True:
            rows = []
            command = device.shell("top -n 1 -d 1 | awk 'NR>5 {print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12}' | sed -E 's/\x1b\[[0-9;]*m//g'")

            output = command.replace("\r","").strip().split("\n")
            for list_args in output:
                split_list = re.split(r'\s+', list_args.strip(), maxsplit=11)
                if "shell" not in split_list and len(split_list) == 12:
                    row = {
                        "PID": split_list[0],
                        "USER": split_list[1],
                        "PR": split_list[2],
                        "NI": split_list[3],
                        "VIRT": split_list[4],
                        "RES": split_list[5],
                        "SHR": split_list[6],
                        "S": split_list[7],
                        "[%CPU]": split_list[8],
                        "%MEM": split_list[9],
                        "TIME+": split_list[10],
                        "ARGS": split_list[11]
                    }
                    rows.append(row)
            time.sleep(1)
            self.append_metrics_data(rows)

def main():

    with open("device_metrics_process_for_android_pid.pid","w") as file:
        file.write(str(os.getpid()))

    device_udid = sys.argv[1]
    file_path = sys.argv[2]
    device_metrics = DeviceMetricsForAndroid(device_udid, file_path)
    device_metrics.start_metrics()

main()