import os
import signal
with open("device_metrics_process_for_ios_pid.pid","r") as file:
    pid = int(file.read())
    os.kill(pid, signal.SIGTERM)