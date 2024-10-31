import subprocess

from sqlalchemy import create_engine
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
