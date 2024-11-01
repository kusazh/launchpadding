from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from launchpadding.model.base import Base


class DownloadingApp(Base):
    """
    CREATE TABLE downloading_apps (
        item_id INTEGER PRIMARY KEY,
        title VARCHAR,
        bundleid VARCHAR,
        storeid VARCHAR,
        category_id INTEGER,
        install_path VARCHAR
    );
    """

    __tablename__ = "downloading_apps"

    item_id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    bundleid = mapped_column(String)
    storeid = mapped_column(String)
    category_id = mapped_column(Integer)
    install_path = mapped_column(String)

    def __repr__(self) -> str:
        return f"<DownloadingApp(item_id={self.item_id}, title={self.title}>"

    @property
    def view_title(self) -> str:
        return self.title if len(self.title) < 13 else self.title[:13] + "..."
