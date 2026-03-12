from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "clinic.db"

EXPORT_DIR = PROJECT_ROOT / "data"

EVENT_EXPORT = EXPORT_DIR / "powerbi_events.csv"
CASE_EXPORT = EXPORT_DIR / "powerbi_case_summary.csv"
STAGE_EXPORT = EXPORT_DIR / "powerbi_stage_delays.csv"


def main():

    conn = sqlite3.connect(DB_PATH)

    events_df = pd.read_sql_query(
        """
        SELECT
            case_id,
            activity,
            timestamp,
            cancer_type,
            priority_level,
            department
        FROM event_log
        ORDER BY case_id, timestamp
        """,
        conn,
    )

    events_df["timestamp"] = pd.to_datetime(events_df["timestamp"])

    events_df.to_csv(EVENT_EXPORT, index=False)

    case_summary = (
        events_df.groupby("case_id")
        .agg(
            start_time=("timestamp", "min"),
            end_time=("timestamp", "max"),
            event_count=("activity", "count"),
            cancer_type=("cancer_type", "first"),
            priority_level=("priority_level", "first"),
        )
        .reset_index()
    )

    case_summary["case_duration_days"] = (
        case_summary["end_time"] - case_summary["start_time"]
    ).dt.days

    case_summary.to_csv(CASE_EXPORT, index=False)

    events_df["next_activity"] = events_df.groupby("case_id")["activity"].shift(-1)
    events_df["next_timestamp"] = events_df.groupby("case_id")["timestamp"].shift(-1)

    stage_delays = events_df.dropna(subset=["next_activity"]).copy()

    stage_delays["delay_days"] = (
        stage_delays["next_timestamp"] - stage_delays["timestamp"]
    ).dt.days

    stage_delays = stage_delays[
        ["activity", "next_activity", "delay_days", "cancer_type", "priority_level"]
    ]

    stage_delays.to_csv(STAGE_EXPORT, index=False)

    conn.close()

    print("Power BI tables exported:")
    print(EVENT_EXPORT)
    print(CASE_EXPORT)
    print(STAGE_EXPORT)


if __name__ == "__main__":
    main()