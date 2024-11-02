import plistlib
import subprocess
from functools import cached_property

from icnsutil import ArgbImage, IcnsFile
from sqlalchemy import Integer, String, Float, LargeBinary
from sqlalchemy.orm import mapped_column

from launchpadding.model.base import Base


# TODO: special apps, e.g. Calendar
SPECIAL_COLOR_APPS: dict[str, tuple[int, int, int]] = {}


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

    @cached_property
    def dir(self) -> str | None:
        # TODO: not very reliable
        ls = subprocess.getoutput(
            f"mdfind -onlyin '/System/Applications' -onlyin '/Applications' -name '{self.title}'"
        ).splitlines()
        return ls[1] if len(ls) > 1 else None

    @cached_property
    def icon(self) -> IcnsFile | None:
        if not self.dir:
            return None
        try:
            with open(f"{self.dir}/Contents/Info.plist", "rb") as f:
                plist_data = plistlib.load(f)
                icon_dir = plist_data.get("CFBundleIconFile") or plist_data.get(
                    "CFBundleIconName"
                )
            assert icon_dir
            if not icon_dir.endswith(".icns"):
                icon_dir = f"{icon_dir}.icns"
            return IcnsFile(f"{self.dir}/Contents/Resources/{icon_dir}")
        except Exception:
            return None

    @cached_property
    def icon_color(self) -> tuple[int, int, int] | None:
        # TODO: maybe `image_data`?
        if (color := SPECIAL_COLOR_APPS.get(self.title)):
            return color
        icon = self.icon
        if not icon:
            return None
        image = None
        for i in sorted(icon.media.values(), reverse=True):
            try:
                image = ArgbImage(data=i)
            except (IndexError, NotImplementedError):
                continue
            else:
                break
        if not image:
            return None
        r, g, b = image.r, image.g, image.b
        for i, a in enumerate(image.a):
            if a == 0:
                r[i] = g[i] = b[i] = 255
        return sum(r) // len(r), sum(g) // len(g), sum(b) // len(b)
