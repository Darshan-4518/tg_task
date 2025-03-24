import subprocess
import sys
from command_formatter import remove_escape_character_from_command_output



class DeviceMetricsForIos:

    def __init__(self, udid, file_path):
        self.udid = udid
        self.file_path = file_path


    def trace_monitoring(self):
        command_of_list_devices = subprocess.run("idevice_id -l", shell=True, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 text=True)

        list_of_connected_device = remove_escape_character_from_command_output(command_of_list_devices)

        if self.udid not in list_of_connected_device:
            print(f"Device with {self.udid} udid is not connected")
            sys.exit(1)

        command = subprocess.Popen(
            f"xcrun xctrace record --template 'Activity Monitor' --device-name {self.udid} --all-processes",
            shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,text=True)

        with open("device_metrics_process_for_ios_pid.pid","w") as file:
            file.write(str(command.pid))

        command.wait()

def main():
    udid = sys.argv[1]
    file_path = sys.argv[2]

    device_metrics_for_ios = DeviceMetricsForIos(udid,file_path)
    device_metrics_for_ios.trace_monitoring()

main()