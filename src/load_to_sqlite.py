import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "raw_event_log.csv"
DB_PATH = PROJECT_ROOT / "db" / "clinic.db"
SCHEMA_PATH = PROJECT_ROOT / "db" / "schema.sql"


def load_schema(connection: sqlite3.Connection) -> None:
    if SCHEMA_PATH.exists():
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema_sql)
    else:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS event_log (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                activity TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                cancer_type TEXT,
                priority_level TEXT,
                department TEXT,
                resource TEXT
            );
            """
        )


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Could not find input CSV: {CSV_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CSV_PATH)

    with sqlite3.connect(DB_PATH) as connection:
        load_schema(connection)

        connection.execute("DELETE FROM event_log;")

        df.to_sql("event_log", connection, if_exists="append", index=False)

        row_count = connection.execute("SELECT COUNT(*) FROM event_log").fetchone()[0]
        case_count = connection.execute("SELECT COUNT(DISTINCT case_id) FROM event_log").fetchone()[0]

        print(f"Loaded data into SQLite database: {DB_PATH}")
        print(f"Rows in event_log: {row_count}")
        print(f"Distinct cases: {case_count}")

        print("\nRows by cancer type:")
        for cancer_type, count in connection.execute(
            """
            SELECT cancer_type, COUNT(*)
            FROM event_log
            GROUP BY cancer_type
            ORDER BY COUNT(*) DESC
            """
        ):
            print(f"  {cancer_type}: {count}")

        print("\nSample rows:")
        sample_rows = connection.execute(
            """
            SELECT case_id, activity, timestamp, cancer_type, priority_level
            FROM event_log
            ORDER BY case_id, timestamp
            LIMIT 10
            """
        ).fetchall()

        for row in sample_rows:
            print(row)


if __name__ == "__main__":
    main()