from __future__ import annotations

import colorsys
import subprocess
from typing import Callable, cast

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from launchpadding.model.app import App
from launchpadding.model.base import Base, get_current_columns, ignore_tragger, session
from launchpadding.model.downloading_app import DownloadingApp
from launchpadding.model.group import Group

TYPE_MAP: dict[int, type[Group | App | DownloadingApp]] = {
    2: Group,
    4: App,
    5: DownloadingApp,
}


class Item(Base):
    __tablename__ = "items"

    rowid = mapped_column(Integer, primary_key=True)
    uuid = mapped_column(String)
    flags = mapped_column(Integer)
    type = mapped_column(Integer)
    parent_id = mapped_column(Integer)
    ordering = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"<Item(rowid={self.rowid}, type={self.type}, parent_id={self.parent_id}, ordering={self.ordering})>"

    @property
    def target(self) -> Group | App | DownloadingApp | None:
        clz = TYPE_MAP.get(self.type)
        if clz:
            return session.query(clz).where(clz.item_id == self.rowid).first()  # type: ignore
        return None

    @property
    def parent(self) -> Item | None:
        return self.__class__.get(self.parent_id)

    @classmethod
    def get(cls, rowid: int) -> Item | None:
        return session.query(cls).where(cls.rowid == rowid).first()

    @classmethod
    def get_multi_by_parent(cls, parent_id: int) -> list[Item]:
        return session.query(cls).where(cls.parent_id == parent_id).all()

    @classmethod
    def get_page_dict(cls) -> dict[int, int]:
        pages = session.query(cls).where(cls.parent_id == 1).all()
        return {item.ordering: item.rowid for item in pages if item.ordering}

    @classmethod
    def get_layout_dict(cls) -> dict[int, list[Item]]:
        return {
            ordering: cls.get_multi_by_parent(rowid)
            for ordering, rowid in cls.get_page_dict().items()
        }

    @classmethod
    def print_layout(cls) -> None:
        d = cls.get_layout_dict()
        column = get_current_columns()
        rs = []
        for page, items in d.items():
            _rs = []
            _rs.append(f"\033[1m==> Page {page}\033[0m")
            for i in range(0, len(items), column):
                titles = [
                    f"[{item.ordering + 1:>2}] {t.view_title if (t := item.target) else ''}"
                    for item in items[i : i + column]
                ]
                _rs.append(("{:16}\t" * len(titles)).format(*titles))
            rs.append("\n".join(_rs))
        print("\n\n".join(rs))

    @classmethod
    def fill(cls) -> None:
        page_dict = cls.get_page_dict()
        for i in range(2, max(page_dict) + 1):
            for item in cls.get_multi_by_parent(page_dict[i]):
                item.parent_id = page_dict[1]
        session.commit()
        subprocess.run(["killall", "Dock"])

    @classmethod
    def reset(cls) -> None:
        subprocess.run(
            ["defaults", "write", "com.apple.dock", "ResetLaunchPad", "-bool", "true"]
        )
        subprocess.run(["killall", "Dock"])

    @classmethod
    def sort(cls, key: Callable, reverse: bool = False) -> None:
        page_dict = cls.get_page_dict()
        items = sum(
            (cls.get_multi_by_parent(rowid) for rowid in page_dict.values()), []
        )
        items.sort(key=key, reverse=reverse)

        with ignore_tragger():
            for i, item in enumerate(items):
                item.parent_id = page_dict[1]
                item.ordering = i
            session.commit()
        subprocess.run(["killall", "Dock"])

    @classmethod
    def sort_by_title(cls, reverse: bool = False) -> None:
        return cls.sort(lambda i: t.title if (t := i.target) else "", reverse=reverse)

    @classmethod
    def sort_by_color(cls, reverse: bool = False) -> None:
        def _key(item: Item) -> tuple[float, float]:
            target = item.target
            if not target or not (image := target.image):
                return 2.0, 2.0
            image = image.convert("RGB").resize((1, 1))
            r, g, b = cast(tuple[int, int, int], image.getpixel((0, 0)))
            h, l, _ = colorsys.rgb_to_hls(r, g, b)

            # consider as white or black icon
            if max([r, g, b]) - min([r, g, b]) < 32:
                if l < 128:
                    h += 1
                else:
                    h -= 1
            return round(h, 1), -l

        return cls.sort(_key, reverse=reverse)
