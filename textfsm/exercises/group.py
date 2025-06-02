import io
import pathlib
import textfsm

template = pathlib.Path("group.textfsm")
data = pathlib.Path("group.txt")

parser = textfsm.TextFSM(io.BytesIO(template.read_bytes()))
records = parser.ParseTextToDicts(data.read_text())

for record in records:  # Post-process MEMBERS
    record["MEMBERS"] = [
        members.strip()
        for members in record["MEMBERS"].split(",")
        if members.strip() or ""
    ]

for record in records:
    print(record)
