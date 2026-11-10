#!/usr/bin/env python3
"""Normalize the monthly Box export without losing unquoted commas in text."""
import csv
import io
import re
from pathlib import Path

HEADER = "company_id,name,identifier,category_id,logo_img_pc,logo_img_mb,type,class_url_pc,class_url_mb,explanation,is_recommend,ir_text_front,interest_rate,ir_unit,ir_text_after,annotation,annotation_modal,order,is_valid,promo_url_pc,promo_url_mb,delete_flag,created_at,updated_at".split(",")
START = re.compile(r"^\d+,[^,]*,[^,]*,\d+,")
REWARD = re.compile(r",([01]),([^,]*),(-?\d+(?:\.\d+)?),(%|点|円),([^,]*),")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

def read_export(input_file):
    lines = Path(input_file).read_text(encoding="utf-8-sig").splitlines()
    if not lines or next(csv.reader([lines[0]])) != HEADER:
        raise ValueError("Unexpected CSV header; no output was written.")
    records, current = [], []
    for line in lines[1:]:
        if START.match(line):
            if current:
                records.append("".join(current))
            current = [line.strip()]
        elif line.strip():
            if not current:
                raise ValueError("Content before the first record.")
            current.append(line.strip())
    if current:
        records.append("".join(current))
    rows = []
    for raw in records:
        first = raw.split(",", 9)
        if len(first) != 10:
            raise ValueError("Incomplete prefix.")
        head, body_tail = first[:9], first[9]
        rest = body_tail.rsplit(",", 7)
        if len(rest) != 8:
            raise ValueError(f"Incomplete tail for company {head[0]}.")
        body, tail = rest[0], rest[1:]
        matches = list(REWARD.finditer(body))
        if len(matches) != 1:
            raise ValueError(f"Ambiguous reward fields for company {head[0]}.")
        match = matches[0]
        annotation = body[match.end():].rsplit(",", 1)
        if len(annotation) != 2:
            raise ValueError(f"Incomplete annotation for company {head[0]}.")
        row = head + [body[:match.start()], *match.groups(), *annotation] + tail
        if (len(row) != 24 or not row[0].isdigit() or not row[3].isdigit()
            or not row[17].isdigit() or row[18] not in ("0", "1")
            or row[21] not in ("0", "1")
            or not DATE.fullmatch(row[22]) or not DATE.fullmatch(row[23])):
            raise ValueError(f"Invalid field structure for company {head[0]}.")
        if not all(v == "NULL" or v.lower().startswith(("https://", "http://", "//")) for v in row[19:21]):
            raise ValueError(f"Invalid URL columns for company {head[0]}.")
        # Every original comma and character remains represented in one field.
        if ",".join(row) != raw:
            raise ValueError(f"Round-trip mismatch for company {head[0]}.")
        rows.append(row)
    if not rows or len({r[0] for r in rows}) != len(rows):
        raise ValueError("Empty export or duplicate company IDs.")
    return rows

def fix_csv(input_file, output_file):
    rows = read_export(input_file)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    result = stream.getvalue()
    if list(csv.reader(io.StringIO(result)))[1:] != rows:
        raise ValueError("Quoted CSV round-trip failed.")
    Path(output_file).write_text(result, encoding="utf-8")
    valid = sum(r[18] == "1" and r[21] == "0" for r in rows)
    print(f"正規化完了: {output_file}")
    print(f"総レコード数: {len(rows)} / 全行24列 / 有効レコード数: {valid}")

if __name__ == "__main__":
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else "20260810_companies.csv"
    destination = sys.argv[2] if len(sys.argv) > 2 else source.replace(".csv", "_fixed.csv")
    fix_csv(source, destination)
