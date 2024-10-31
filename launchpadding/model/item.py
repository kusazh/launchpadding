from __future__ import annotations

import subprocess

from sqlalchemy import Column, Integer, String

from launchpadding.model.base import Base, session
from launchpadding.model.app import App
from launchpadding.model.downloading_app import DownloadingApp
from launchpadding.model.group import Group


TYPE_MAP = {2: Group, 4: App, 5: DownloadingApp}


class Item(Base):
    """
    CREATE TABLE items (
        rowid INTEGER PRIMARY KEY ASC,
        uuid VARCHAR,
        flags INTEGER,
        type INTEGER,
        parent_id INTEGER NOT NULL,
        ordering INTEGER
    );
    """

    __tablename__ = "items"

    rowid = Column(Integer, primary_key=True)
    uuid = Column(String)
    flags = Column(Integer)
    type = Column(Integer)
    parent_id = Column(Integer)
    ordering = Column(Integer)

    def __repr__(self) -> str:
        return f"<Item(rowid={self.rowid}, type={self.type}, parent_id={self.parent_id}, ordering={self.ordering})>"

    @property
    def target(self) -> Group | App | DownloadingApp | None:
        clz = TYPE_MAP.get(self.type)
        if clz:
            return session.query(clz).where(clz.item_id == self.rowid).first()
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
    def get_multi_by_page(cls, page: int) -> list[Item]:
        return cls.get_multi_by_parent(cls.get_page_dict()[page])

    @classmethod
    def get_page_dict(cls) -> dict[int, int]:
        pages = session.query(cls).where(cls.parent_id == 1).all()
        return {item.ordering: item.rowid for item in pages if item.ordering}

    def _update(self, **kwargs: int | str) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
        session.commit()

    @classmethod
    def get_layout_dict(cls) -> dict[int, list[Item]]:
        return {
            ordering: cls.get_multi_by_parent(rowid)
            for ordering, rowid in cls.get_page_dict().items()
        }

    @classmethod
    def print_layout(cls, column: int = 7) -> None:
        d = cls.get_layout_dict()
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
    def fill(cls, page_size: int = 35) -> None:
        page_dict = cls.get_page_dict()
        previous_slots = 0
        for i in range(1, max(page_dict) + 1):
            items = cls.get_multi_by_parent(page_dict[i])
            if previous_slots:
                for item in items[-previous_slots:]:
                    item._update(parent_id=page_dict[i - 1])
            previous_slots += page_size - len(items)
        subprocess.run(["killall", "Dock"])

    @classmethod
    def reset(cls) -> None:
        subprocess.run(
            ["defaults", "write", "com.apple.dock", "ResetLaunchPad", "-bool", "true"]
        )
        subprocess.run(["killall", "Dock"])
