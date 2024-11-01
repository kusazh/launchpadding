from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from launchpadding.model.base import Base


class Group(Base):
    """
    CREATE TABLE groups (
        item_id INTEGER PRIMARY KEY,
        category_id INTEGER,
        title VARCHAR
    );
    """

    __tablename__ = "groups"

    item_id = mapped_column(Integer, primary_key=True)
    category_id = mapped_column(Integer)
    title = mapped_column(String)

    def __repr__(self) -> str:
        return f"<Group(item_id={self.item_id}, title={self.title})>"

    @property
    def view_title(self) -> str:
        title = self.title if len(self.title) < 13 else self.title[:13] + "..."
        return f"[{title}]"

    @property
    def targets(self) -> list:
        from launchpadding.model.item import Item

        items = Item.get_multi_by_parent(int(self.item_id + 1))
        return [item.target for item in items]
