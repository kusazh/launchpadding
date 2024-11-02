import subprocess
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# get Launchpad db path
db_path = subprocess.getoutput(
    "echo /private$(getconf DARWIN_USER_DIR)com.apple.dock.launchpad/db/db"
)
engine = create_engine(f"sqlite:///{db_path}", echo=False)  # echo=True when debugging

Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


@contextmanager
def ignore_tragger():
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE dbinfo SET value=1 WHERE key='ignore_items_update_triggers'")
        )
        conn.commit()

        try:
            yield
        finally:
            conn.execute(
                text(
                    "UPDATE dbinfo SET value=0 WHERE key='ignore_items_update_triggers'"
                )
            )
            conn.commit()


def get_current_columns() -> int:
    try:
        return int(
            subprocess.getoutput("defaults read com.apple.dock springboard-columns")
        )
    except ValueError:
        return 7
