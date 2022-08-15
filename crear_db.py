import sqlite3
import pandas as pd


def execute_script(cur: str, script_filepath: str) -> None:
    """This function execute a script in the database.
    Args:
        db_uri (str): a database uri.
        script_filepath (str): file path to the script to execute.
    """

    with open(script_filepath, "r") as f:
        script = f.read()
    cur.executescript(script)


def upload_languages(csv_path: str, cur) -> None:

    lines = []
    with open(csv_path, "r") as f:
        for line in f:
            lines.append(line.strip())

    lines = set(lines)
    for line in lines:
        cur.execute("INSERT INTO Languages (name) VALUES (?)", (line.strip(),))


def upload_countries(csv_path: str, cur) -> None:
    lines = []
    with open(csv_path, "r") as f:
        for line in f:
            lines.append(line.strip())

    lines = set(lines)
    for line in lines:
        cur.execute("INSERT INTO Countries (name) VALUES (?)", (line.strip(),))


def show_db():
    """Prints all data in database including all table names, column names and data."""
    conn = sqlite3.connect("WorldLanguages.sqlite")
    cur = conn.cursor()

    # Get all table names
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()
    tables.remove(("sqlite_sequence",))

    # Iterate over all tables
    print("PRINTING ALL TABLES")
    for table_name in tables:
        # print table name and column names
        print(f"NAME : {table_name[0]}")
        print("COLUMNS :", end="")
        for col in cur.execute(f"PRAGMA table_info({table_name[0]})").fetchall():
            print(f" {col[1]}", end="")
        print()

        # print the data
        for row in cur.execute(f"SELECT * FROM {table_name[0]}"):
            print(row)
        print("-" * 50)

    # close connection to database
    conn.close()


def upload_regions(csv_path: str, cur) -> None:
    countries = []
    regions = []

    with open(csv_path) as f:
        f.readline()
        for line in f:
            x = line.replace('"', "").split(",")
            countries.append(x[0])
            regions.append(x[1])

    # subir regiones
    regions_set = set([r.strip() for r in regions])
    for r in regions_set:
        cur.execute("INSERT INTO Regions (name) VALUES (?)", (r.strip(),))

    # subir regions_countries
    for r, c in zip(regions, countries):
        c_id = cur.execute(
            "SELECT id FROM Countries WHERE name = ?", (c.strip(),)
        ).fetchone()
        r_id = cur.execute(
            "SELECT id FROM Regions WHERE name = ?", (r.strip(),)
        ).fetchone()

        if c_id and r_id:
            cur.execute(
                "INSERT INTO Regions_Countries (country_id, region_id) VALUES (?, ?)",
                (c_id[0], r_id[0]),
            )


def load_all_data(folder_path: str, cur) -> None:
    """Loads all data from a folder.
    Args:
        folder_path (str): path to the folder.
    """
    import os

    countries = os.listdir(folder_path)
    for country in countries:
        # print(country)
        data = load_datafile(f"{folder_path}/{country}/data.csv")
        data = data.astype({"year": int})
        # print(data.head())

        yearly_data = os.listdir(f"{folder_path}/{country}/")
        yearly_data.remove("data.csv")

        for y_data in yearly_data:
            year = y_data.split(".")[0].split(" ")[-1]
            country_population = data[data["year"] == int(year)]["speakers"].sum()
            # print(country, year, country_population, end=" ")
            with open(f"{folder_path}/{country}/{y_data}", "r", encoding="utf8") as f:
                for line in f:
                    local_speakers = int(float(line.split(",")[1].strip()))
                    language = line.split(",")[2].strip()
                    # print(language, local_speakers)

                    c_id = cur.execute(
                        "SELECT id FROM Countries WHERE name = ?", (country.strip(),)
                    ).fetchone()
                    l_id = cur.execute(
                        "SELECT id FROM Languages WHERE name = ?", (language.strip(),)
                    ).fetchone()

                    if c_id and l_id:
                        cur.execute(
                            "INSERT INTO Captures (country_id, language_id, year, local_speakers, country_population) VALUES (?, ?, ?, ?, ?)",
                            (
                                c_id[0],
                                l_id[0],
                                int(year),
                                int(local_speakers),
                                int(country_population),
                            ),
                        )


def load_datafile(filepath: str):
    return pd.read_csv(filepath, header=None, names=["name", "year", "speakers"])


def upload_official_languages(csv_path: str, cur) -> None:
    lines = []
    with open(csv_path, "r") as f:
        for line in f:
            lines.append(line.strip())

    for line in lines:
        c_id = cur.execute(
            "SELECT id FROM Countries WHERE name = ?", (line.split(",")[0].strip(),)
        ).fetchone()

        for i in line.split(",")[1:]:
            l_id = cur.execute(
                "SELECT id FROM Languages WHERE name = ?", (i.strip(),)
            ).fetchone()
            if c_id and l_id:
                cur.execute(
                    "INSERT INTO Official_Languages (country_id, language_id) VALUES (?, ?)",
                    (c_id[0], l_id[0]),
                )


def upload_speakers(folder_path: str, cur) -> None:
    import os

    for filepath in os.listdir(folder_path):
        with open(f"{folder_path}/{filepath}") as f:
            f.readline()
            for line in f:
                # llenar linea en speakers
                if line.split(",")[1].strip() == "":
                    continue
                year = filepath.split(".")[0].split(" ")[-1]
                native_speakers = int(float(line.split(",")[1].strip()))
                total_speakers = int(float(line.split(",")[2].strip()))

                language = line.split(",")[3].strip()

                cur.execute(
                    "INSERT INTO Speakers (year, native_speakers, total_speakers) VALUES (?, ?, ?)",
                    (int(year), native_speakers, total_speakers),
                )

                s_id = cur.execute(
                    "SELECT id FROM Speakers WHERE year = ? AND native_speakers = ?",
                    (int(year), native_speakers),
                ).fetchone()

                # llenar linea en speakers_countries
                cur.execute(
                    "INSERT INTO Speakers_Countries (speaker_id, country_id) VALUES (?, ?)",
                    (s_id[0], 1),
                )


def main() -> None:
    db_manager = "WorldLanguages.sqlite"
    db_conn = sqlite3.connect(db_manager, isolation_level=None)
    db_cur = db_conn.cursor()

    execute_script(db_cur, "crear_db.sql")

    upload_languages("db\languagelist.csv", db_cur)

    upload_countries("db\countrieslist.csv", db_cur)

    upload_regions("db\\regions_countries.csv", db_cur)

    load_all_data("data_final", db_cur)

    upload_official_languages("db\Languages.txt", db_cur)

    upload_speakers("db\speakers", db_cur)

    # show_db()


if __name__ == "__main__":
    main()
