from sqlalchemy import Column, Integer, String, Float, LargeBinary

from launchpadding.model.base import Base


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

    __tablename__ = "apps"

    item_id = Column(Integer, primary_key=True)
    title = Column(String)
    bundleid = Column(String)
    storeid = Column(String)
    category_id = Column(Integer)
    moddate = Column(Float)
    bookmark = Column(LargeBinary)

    def __repr__(self) -> str:
        return f"<App(item_id={self.item_id}, title={self.title}>"

    @property
    def view_title(self) -> str:
        return str(self.title if len(self.title) < 13 else self.title[:13] + "...")
