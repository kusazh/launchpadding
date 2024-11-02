from functools import cached_property
from io import BytesIO

from PIL import Image
from sqlalchemy import Integer, LargeBinary
from sqlalchemy.orm import MappedColumn, mapped_column

from launchpadding.model.base import Base, session


class ImageCache(Base):
    __tablename__ = "image_cache"

    item_id = mapped_column(Integer, primary_key=True)
    size_big = mapped_column(Integer)
    size_mini = mapped_column(Integer)
    image_data = mapped_column(LargeBinary)
    image_data_mini = mapped_column(LargeBinary)


class ImageCacheMixin:
    item_id: MappedColumn[int]

    @cached_property
    def image(self) -> Image.Image | None:
        ic = session.query(ImageCache).where(ImageCache.item_id == self.item_id).first()
        if ic:
            stream = BytesIO(ic.image_data_mini)
            return Image.open(stream)
        else:
            return None
