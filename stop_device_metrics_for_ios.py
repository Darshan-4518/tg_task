import os
import shutil
import signal
import subprocess
import time
from command_formatter import remove_escape_character_from_command_output
from xml.etree import ElementTree  as ET
import csv

with open("device_metrics_process_for_ios_pid.pid","r") as file:
    pid = int(file.read())

os.kill(pid,signal.SIGINT)
time.sleep(60)

command = subprocess.run("ls | grep .trace",shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
trace_file_name = remove_escape_character_from_command_output(command)


command_to_transfer_in_xml_file = f"""xcrun xctrace export --input {trace_file_name} --output  output.xml  --xpath '/trace-toc/run[@number="1"]/data/table[@schema="activity-monitor-process-live"]'"""
command_output = subprocess.run(command_to_transfer_in_xml_file,shell=True,stdout=subprocess.PIPE,text=True)

shutil.rmtree(trace_file_name)

xml_file = "output.xml"

parsed_xml_file = ET.parse(xml_file)

headers = ["process_name","cpu(%)","memory(bytes)"]
rows = []
for row in parsed_xml_file.getroot().findall(".//row"):
    process = row.find("process")
    cpu_percent = row.findtext("system-cpu-percent")
    size_in_bytes = row.findtext("size-in-bytes")

    if "fmt" in process.attrib:
        rows.append([process.attrib['fmt'].split(" ")[0],cpu_percent or 0,size_in_bytes or 0])


with open("metrics_data_of_ios.csv","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)