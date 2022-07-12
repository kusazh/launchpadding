from sqlalchemy import Column, Integer, String

from launchpadding.model.base import Base, session
from launchpadding.model.app import App
from launchpadding.model.downloading_app import DownloadingApp
from launchpadding.model.group import Group


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

    __tablename__ = 'items'

    TYPE_MAP = {
        2: Group,
        4: App,
        5: DownloadingApp
    }

    rowid = Column(Integer, primary_key=True)
    uuid = Column(String)
    flags = Column(Integer)
    type = Column(Integer)
    parent_id = Column(Integer)
    ordering = Column(Integer)

    def __repr__(self):
        return "<Item(rowid='%s', type='%s', parent_id='%s', ordering='%s')>" % (
            self.rowid, self.type, self.parent_id, self.ordering
        )

    @property
    def target(self):
        obj = self.TYPE_MAP.get(self.type, None)
        return session.query(obj).where(obj.item_id == self.rowid).first() if obj else None

    @classmethod
    def get_layout_dict(cls):
        items = session.query(cls).where(cls.parent_id == 1).all()
        d = {item.ordering: item.rowid for item in items if item.ordering}
        for ordering, rowid in d.items():
            items = session.query(cls).where(cls.parent_id == rowid).all()
            d[ordering] = [(item.ordering, item.target) for item in items]
        return d

    @classmethod
    def get_layout(cls, width=7):
        d = cls.get_layout_dict()
        for page, items in d.items():
            print(f'\033[1m==> Page {page}\033[0m')
            for i in range(0, len(items), width):
                titles = [
                    f'[{ordering + 1:>2}] {target.view_title}'
                    for ordering, target in items[i:i + width]
                ]
                print(('{:16}\t' * len(titles)).format(*titles))
            print('\n')
