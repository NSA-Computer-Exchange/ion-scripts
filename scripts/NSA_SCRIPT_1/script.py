import csv
from io import StringIO
import xml.etree.ElementTree as ET

# Sample CSV data
csv_data = data_in.strip()  

# Read CSV using StringIO
csv_file = StringIO(csv_data)
reader = csv.DictReader(csv_file)

# Root XML element
root = ET.Element("products")

# Convert rows
for row in reader:
    item = ET.SubElement(root, "PRODS_YO")
    for key, value in row.items():
        field = ET.SubElement(item, key)
        field.text = value

# Convert XML tree to string
xml_output = ET.tostring(root, encoding="unicode")

data_out = xml_output