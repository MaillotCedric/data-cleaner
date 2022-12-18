from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_engine():
    url = URL.create(
        drivername="postgresql",
        username="postgres",
        host="127.0.0.1",
        database="afpar",
        password="0000"
    )

    return create_engine(url)
