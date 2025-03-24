import csv
import xml.etree.ElementTree as ET
from os import PRIO_PROCESS

xml_file = "output.xml"

parsed_xml_file = ET.parse(xml_file)

headers = ["process_name","cpu","memory(bytes)"]
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