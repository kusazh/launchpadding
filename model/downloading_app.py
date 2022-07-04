from sqlalchemy import Column, Integer, String

from model.base import Base


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

    __tablename__ = 'downloading_apps'

    item_id = Column(Integer, primary_key=True)
    title = Column(String)
    bundleid = Column(String)
    storeid = Column(String)
    category_id = Column(Integer)
    install_path = Column(String)

    def __repr__(self):
        return (
            "<DownloadingApp(item_id='%s', title='%s', bundleid='%s', storeid='%s', category_id='%s'>" % (
                self.item_id, self.title, self.bundleid, self.storeid, self.category_id
            )
        )
