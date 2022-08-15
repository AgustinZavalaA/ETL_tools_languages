import sys
import pandas as pd
import numpy as np
import enum


class NullCheckerType(enum.Enum):
    check_null = "check_null"
    check_zero = "check_zero"
    check_negative = "check_negative"
    check_empty_str = "check_empty_str"


def null_eliminator(csv_filename: str, types_to_check: list[str], out_filename:str="") -> None:
    print("Eliminador de filas con valores nulos")
    # load csv
    df = pd.read_csv(csv_filename)

    if NullCheckerType.check_zero.name in types_to_check:
        df = df.replace(0, np.nan)

    if NullCheckerType.check_negative.name in types_to_check:
        # df[ < 0] = np.nan
        df[df[df.select_dtypes([np.number]).columns] < 0] = np.nan
    if NullCheckerType.check_empty_str.name in types_to_check:
        df = df.replace("^[^\w]$", np.nan, regex=True)

    # eliminate rows with null values
    df = df.dropna(axis=0, how="any")
    # save csv
    if out_filename:
        df.to_csv(out_filename, index=False)
    else:
        df.to_csv(f"{csv_filename.split('.')[0]}_null.csv", index=False)


if __name__ == "__main__":
    null_eliminator(sys.argv[1], sys.argv[2:])
