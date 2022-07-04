from sqlalchemy import Column, Integer, String, Float, LargeBinary

from model.base import Base


class App(Base):
    """
    CREATE TABLE apps (
        item_id INTEGER PRIMARY KEY,
        title VARCHAR,
        bundleid VARCHAR,
        storeid VARCHAR,
        category_id INTEGER,
        moddate REAL,
        bookmark BLOB
    );
    """

    __tablename__ = 'apps'

    item_id = Column(Integer, primary_key=True)
    title = Column(String)
    bundleid = Column(String)
    storeid = Column(String)
    category_id = Column(Integer)
    moddate = Column(Float)
    bookmark = Column(LargeBinary)

    def __repr__(self):
        return (
            "<App(item_id='%s', title='%s', bundleid='%s', storeid='%s', category_id='%s', moddate='%s'>" % (
                self.item_id, self.title, self.bundleid, self.storeid, self.category_id, self.moddate
            )
        )
