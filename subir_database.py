import pandas as pd
import sys
from sqlalchemy import create_engine


def upload_database(csv_filename: str) -> None:
    df = pd.read_csv(csv_filename)

    engine = create_engine("sqlite://", echo=False)

    df.to_sql("captures", con=engine)
    engine.execute("SELECT * FROM captures").fetchall()


if __name__ == "__main__":
    upload_database(sys.argv[1])
