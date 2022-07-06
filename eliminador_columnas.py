import sys
import pandas as pd
import numpy as np


def column_eliminator(csv_filename: str, columns_to_save: list[str], replace_file: bool = True) -> None:
    print("Eliminador de columnas")
    # load csv
    df = pd.read_csv(csv_filename)
    # get columns to save
    df = df[columns_to_save]
    # save csv
    if replace_file:
        df.to_csv(f"{csv_filename.split('.')[0]}_col.csv", index=False)


if __name__ == "__main__":
    print(sys.argv)
    column_eliminator(sys.argv[1], sys.argv[2:])
