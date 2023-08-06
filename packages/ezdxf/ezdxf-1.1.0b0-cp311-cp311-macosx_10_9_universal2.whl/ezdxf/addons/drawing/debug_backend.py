#  Copyright (c) 2021-2022, Manfred Moitzi
#  License: MIT License
from __future__ import annotations
from typing import Iterable
from ezdxf.math import AnyVec
from ezdxf.path import Path, Path2d
from .properties import Properties
from .backend import Backend
from .config import Configuration


class BasicBackend(Backend):
    """The basic backend has no draw_path() support and approximates all curves
    by lines.
    """

    def __init__(self):
        super().__init__()
        self.collector = []
        self.configure(Configuration.defaults())

    def draw_point(self, pos: AnyVec, properties: Properties) -> None:
        self.collector.append(("point", pos, properties))

    def draw_line(self, start: AnyVec, end: AnyVec, properties: Properties) -> None:
        self.collector.append(("line", start, end, properties))

    def draw_filled_polygon(
        self, points: Iterable[AnyVec], properties: Properties
    ) -> None:
        self.collector.append(("filled_polygon", list(points), properties))

    def set_background(self, color: str) -> None:
        self.collector.append(("bgcolor", color))

    def clear(self) -> None:
        self.collector = []


class PathBackend(BasicBackend):
    def draw_path(self, path: Path | Path2d, properties: Properties) -> None:
        self.collector.append(("path", path, properties))
