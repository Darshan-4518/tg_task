import subprocess
import sys

device_udid = sys.argv[1]
file_path = sys.argv[2]

subprocess.Popen(f"python device_performance_metrics_for_ios.py {device_udid} {file_path}",text=True,shell=True)
