import csv
import io

import orjson

import enerbitdso.enerbit as enerbit


def as_json(records: list[enerbit.ScheduleUsageRecord]) -> io.StringIO:
    content = orjson.dumps([r.dict() for r in records])
    res = io.BytesIO(content)
    wrapper = io.TextIOWrapper(res, encoding="utf-8")
    return wrapper


def as_csv(records: list[enerbit.ScheduleUsageRecord], header: bool) -> io.StringIO:
    res = io.StringIO(newline="")
    fields = records[0].__fields__.keys()
    content_lines = [r.dict() for r in records]
    writer = csv.DictWriter(res, fields, lineterminator="\n")
    if header:
        writer.writeheader()
    for i in content_lines:
        writer.writerow(i)
    return res


def as_jsonl(records: list[enerbit.ScheduleUsageRecord]) -> io.StringIO:
    content_lines = [orjson.dumps(r.dict()) for r in records]
    res = io.BytesIO()
    for i in content_lines:
        res.write(i)
        res.write(b"\n")
    wrapper = io.TextIOWrapper(res, encoding="utf-8")
    return wrapper
