import subprocess
import sys

device_udid = sys.argv[1]
file_path = sys.argv[2]

command = subprocess.Popen(f"python device_performance_metrics_for_android.py {device_udid} {file_path}",stdout=subprocess.PIPE,text=True,shell=True)
