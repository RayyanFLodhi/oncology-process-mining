import sqlite3
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "clinic.db"

RAW_EXPORT = PROJECT_ROOT / "data" / "processed_event_log.csv"
PM4PY_EXPORT = PROJECT_ROOT / "data" / "pm4py_event_log.csv"


def main():

    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run load_to_sqlite.py first.")

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        case_id,
        activity,
        timestamp,
        cancer_type,
        priority_level,
        department,
        resource
    FROM event_log
    ORDER BY case_id, timestamp
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values(["case_id", "timestamp"])

    df.to_csv(RAW_EXPORT, index=False)

    pm4py_df = df.rename(
        columns={
            "case_id": "case:concept:name",
            "activity": "concept:name",
            "timestamp": "time:timestamp",
        }
    )

    pm4py_df = pm4py_df[
        [
            "case:concept:name",
            "concept:name",
            "time:timestamp",
            "cancer_type",
            "priority_level",
            "department",
        ]
    ]

    pm4py_df.to_csv(PM4PY_EXPORT, index=False)

    print(f"Processed event log saved: {RAW_EXPORT}")
    print(f"PM4Py formatted event log saved: {PM4PY_EXPORT}")
    print(f"Total events: {len(pm4py_df)}")
    print(f"Total cases: {pm4py_df['case:concept:name'].nunique()}")

    print("\nSample rows:")
    print(pm4py_df.head(10))


if __name__ == "__main__":
    main()