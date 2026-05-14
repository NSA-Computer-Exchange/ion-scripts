import csv
import xml.etree.ElementTree as ET
from io import StringIO

data_in = ""
def main(data_in):
    """Parse XML input string and return CSV string output."""

    root = ET.fromstring(data_in)

    rows = list(root)
    if not rows:
        return ""

    first_record = rows[0]
    headers = [child.tag for child in first_record]

    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(headers)

    for record in rows:
    
        values = [record.find(h).text if record.find(h) is not None else "" for h in headers]
        values1 = str(123)
        writer.writerow(values+ [values1])

    return out.getvalue()

data_out = main(data_in)
