from sqlalchemy import Column, Integer, String

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

    item_id = Column(Integer, primary_key=True)
    title = Column(String)
    bundleid = Column(String)
    storeid = Column(String)
    category_id = Column(Integer)
    install_path = Column(String)

    def __repr__(self) -> str:
        return f"<DownloadingApp(item_id={self.item_id}, title={self.title}>"

    @property
    def view_title(self) -> str:
        return str(self.title if len(self.title) < 13 else self.title[:13] + "...")
