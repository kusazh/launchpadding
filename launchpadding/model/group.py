from sqlalchemy import Column, Integer, String

from launchpadding.model.base import Base, session


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

    def __repr__(self):
        return "<Group(item_id='%s', title='%s')>" % (self.item_id, self.title)

    @property
    def view_title(self):
        _view_title = self.title if len(self.title) < 13 else self.title[:13] + "..."
        return f"[{_view_title}]"

    # @property
    # def targets(self):
    #     from model.item import Item

    #     parent = session.query(Item).where(Item.parent_id == self.item_id).first()
    #     items = session.query(Item).where(Item.parent_id == parent.rowid).all()
    #     return [item.target for item in items]
