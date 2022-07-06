import sys
import pandas as pd
import numpy as np
import random


def duplicates_eliminator(csv_filename: str, strategy: str, columns_to_consider: list[str] = None) -> None:
    print("Eliminador de duplicados")
    # load csv
    df = pd.read_csv(csv_filename)
    # get columns to save
    if strategy == "select_random":
        if columns_to_consider:
            if random.random() > 0.5:
                df = df.drop_duplicates(subset=columns_to_consider, keep="first")
            else:
                df = df.drop_duplicates(subset=columns_to_consider, keep="last")
        else:
            if random.random() > 0.5:
                df = df.drop_duplicates(keep="first")
            else:
                df = df.drop_duplicates(keep="last")

    # save csv
    df.to_csv(f"{csv_filename.split('.')[0]}_dup.csv", index=False)


if __name__ == "__main__":
    duplicates_eliminator(sys.argv[1], sys.argv[2], sys.argv[3:])
