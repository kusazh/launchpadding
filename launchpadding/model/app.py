from sqlalchemy import Integer, String, Float, LargeBinary
from sqlalchemy.orm import mapped_column

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

    item_id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    bundleid = mapped_column(String)
    storeid = mapped_column(String)
    category_id = mapped_column(Integer)
    moddate = mapped_column(Float)
    bookmark = mapped_column(LargeBinary)

    def __repr__(self) -> str:
        return f"<App(item_id={self.item_id}, title={self.title}>"

    @property
    def view_title(self) -> str:
        return self.title if len(self.title) < 13 else self.title[:13] + "..."
