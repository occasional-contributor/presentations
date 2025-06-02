import io
import pathlib

import textfsm

template = pathlib.Path("passwd.textfsm")
data = pathlib.Path("passwd.txt")

parser = textfsm.TextFSM(io.BytesIO(template.read_bytes()))
records = parser.ParseTextToDicts(data.read_text())

for record in records:
    print(record)
