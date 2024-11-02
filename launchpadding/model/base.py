import subprocess
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# get Launchpad db path
user_dir = subprocess.run(
    ["getconf", "DARWIN_USER_DIR"], capture_output=True, text=True
).stdout.strip()

engine = create_engine(
    f"sqlite:////private{user_dir}com.apple.dock.launchpad/db/db", echo=False
)  # echo=True when debugging

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
            subprocess.run(
                ["defaults", "read", "com.apple.dock", "springboard-columns"],
                capture_output=True,
                text=True,
            ).stdout.strip()
        )
    except ValueError:
        return 7
