import csv
import xml.etree.ElementTree as ET
from io import StringIO

data_in = ""
## More comments from the peanut gallery
def main(data_in):
    """Parse XML input string and return CSV string output."""
    # data_in should be XML text with repeating element records
    # e.g. <root><row><a>1</a><b>2</b></row><row>...</row></root>
    root = ET.fromstring(data_in)

    # Find first child element that represents a row/record
    rows = list(root)
    if not rows:
        return ""

    # Use keys from first record child tags
    first_record = rows[0]
    headers = [child.tag for child in first_record]

    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(headers)

    for record in rows:
        # fallback to empty string for missing tags
        values = [record.find(h).text if record.find(h) is not None else "" for h in headers]
        values1 = str(123)
        writer.writerow(values+ [values1])

    return out.getvalue()

data_out = main(data_in)
