from sqlalchemy import Column, Integer, String

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

    item_id = Column(Integer, primary_key=True)
    category_id = Column(Integer)
    title = Column(String)

    def __repr__(self) -> str:
        return f"<Group(item_id={self.item_id}, title={self.title})>"

    @property
    def view_title(self) -> str:
        title = self.title if len(self.title) < 13 else self.title[:13] + "..."
        return f"[{title}]"

    @property
    def targets(self) -> list:
        from launchpadding.model.item import Item

        items = Item.get_multi_by_parent(self.item_id + 1)
        return [item.target for item in items]
