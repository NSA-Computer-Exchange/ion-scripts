import json
from io import StringIO

def build_payload_from_invoice(invoice_json):
    if isinstance(invoice_json, str):
        invoice_json = json.loads(invoice_json)

    hdr = invoice_json["invoice"]["InvoiceHeader"]

    order_no = hdr["OrderNo"]
    order_suffix = int(hdr["OrderSuffix"])

    buf = StringIO()

    buf.write('{')
    buf.write('"queries":{')
    buf.write('"query":[{')
    buf.write('"entities":"Attachments",')
    buf.write('"useTextSearch":false,')
    buf.write('"arguments":{')
    buf.write('"argument":[')

    buf.write(json.dumps({
        "key": "Order_Number",
        "operator": "=",
        "value": order_no,
        "logicalType": ""
    }))
    buf.write(',')

    buf.write(json.dumps({
        "key": "Order_Suffix",
        "operator": "=",
        "value": order_suffix,
        "logicalType": "AND"
    }))

    buf.write(']}')
    buf.write('}]')
    buf.write('}}')

    payload = json.loads(buf.getvalue())
    buf.close()

    return json.dumps(payload, indent=2)

data_out = build_payload_from_invoice(data_in)