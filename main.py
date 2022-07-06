import json
import sys

from eliminador_nulos import null_eliminator
from eliminador_columnas import column_eliminator


def main(json_file) -> None:
    """
    Main function.
    """
    with open(json_file) as f:
        data = json.load(f)
    print(json.dumps(data, indent=4))

    for script in data["scripts"]:
        print(script)
        print(data["scripts"][script])

        for file_args in data["scripts"][script]:
            print(file_args["file"])
            print(file_args["args"])

            if script == "eliminador_columnas.py":
                column_eliminator(file_args["file"], file_args["args"])
            elif script == "eliminador_nulos.py":
                null_eliminator(file_args["file"], file_args["args"])


if __name__ == "__main__":
    main(sys.argv[1])
