import sys
import pandas as pd
import numpy as np


def column_eliminator(
    csv_filename: str, columns_to_save: list[str], output_filename: str = ""
) -> None:
    print("Eliminador de columnas")
    # load csv
    df = pd.read_csv(csv_filename)
    # get columns to save
    print(df.columns)
    df = df[columns_to_save]
    # save csv
    if output_filename:
        df.to_csv(output_filename, index=False)
    else:
        df.to_csv(f"{csv_filename.split('.')[0]}_col.csv", index=False)


if __name__ == "__main__":
    print(sys.argv)
    column_eliminator(sys.argv[1], sys.argv[2:])
