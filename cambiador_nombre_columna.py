import sys
import pandas as pd
import numpy as np


def column_name_changer(
    csv_filename: str, columns: list[str], out_filename: str = ""
) -> None:
    print("Cambiador de nombres de columnas")
    # load csv
    df = pd.read_csv(csv_filename)

    rename_dict = {columns[i]: columns[i + 1] for i in range(0, len(columns), 2)}
    df.rename(columns=rename_dict, inplace=True)

    if out_filename:
        print(f"Saving to {out_filename}")
        df.to_csv(out_filename, index=False)
    else:
        df.to_csv(f"{csv_filename.split('.')[0]}_ncol.csv", index=False)


if __name__ == "__main__":
    column_name_changer(sys.argv[1], sys.argv[2:])
