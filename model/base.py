import subprocess

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# get Launchpad db path
db_path = subprocess.getoutput('echo /private$(getconf DARWIN_USER_DIR)com.apple.dock.launchpad/db/db')
engine = create_engine('sqlite:///' + db_path, echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
