from __future__ import annotations

from collections.abc import Iterator
from json import loads
from pathlib import Path
from re import split
from typing import Final
from typing import TypeAlias
from typing import TypedDict

from visual_novel_toolkit.workspace import internal_directory


report_file: Final = internal_directory / "yaspeller_report.json"


def load_mistakes() -> set[str]:
    if not report_file.exists():
        return set()

    content = report_file.read_text()
    report: Report = loads(content)

    return set(flatten_report(report))


def flatten_report(report: Report) -> Iterator[str]:
    for each in report:
        text = resource_text(each[1])
        for item in each[1]["data"]:
            if item["word"] in text:
                yield item["word"]


def resource_text(items: Items) -> set[str]:
    resource = Path(items["resource"])
    if resource.exists():
        words: list[str] = split(r"\W+", resource.read_text())
        return set(words)
    else:
        return set()


class Item(TypedDict):
    word: str


class Items(TypedDict):
    resource: str
    data: list[Item]


Report: TypeAlias = list[tuple[bool, Items]]
