import json
import sys

from eliminador_nulos import null_eliminator
from eliminador_columnas import column_eliminator
from eliminador_duplicados import duplicates_eliminator
from cambiador_nombre_columna import column_name_changer
from subir_database import upload_database


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
                if "out" in file_args.keys():
                    print(file_args["out"])
                    column_eliminator(
                        file_args["file"], file_args["args"], file_args["out"]
                    )
                else:
                    column_eliminator(file_args["file"], file_args["args"])
            elif script == "eliminador_nulos.py":
                null_eliminator(file_args["file"], file_args["args"], file_args["out"])
            elif script == "eliminador_duplicados.py":
                if "cols" in file_args.keys():
                    duplicates_eliminator(
                        file_args["file"],
                        file_args["args"],
                        file_args["cols"],
                        file_args["out"],
                    )
                else:
                    duplicates_eliminator(
                        file_args["file"], file_args["args"], file_args["out"]
                    )

            # no probado
            elif script == "cambiador_nombre_columna.py":
                print(file_args["args"])
                print(file_args["out"])
                column_name_changer(
                    file_args["file"], file_args["args"], file_args["out"]
                )

            elif script == "subir_database.py":
                upload_database(file_args["file"])


if __name__ == "__main__":
    main(sys.argv[1])
