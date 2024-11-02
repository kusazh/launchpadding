from sqlalchemy import Float, Integer, LargeBinary, String
from sqlalchemy.orm import mapped_column

from launchpadding.model.base import Base
from launchpadding.model.image_cache import ImageCacheMixin


class App(Base, ImageCacheMixin):
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
