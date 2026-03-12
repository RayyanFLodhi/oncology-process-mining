import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw_event_log.csv"

random.seed(42)

ACTIVITY_FLOW = [
    ("Referral Received", "Referral Office"),
    ("Intake Review", "Referral Office"),
    ("Initial Consultation", "Oncology"),
    ("Diagnostic Imaging", "Radiology"),
    ("Diagnosis Confirmed", "Pathology"),
    ("Treatment Planning", "Oncology"),
    ("Treatment Start", "Treatment Unit"),
    ("Follow-Up", "Oncology"),
]

CANCER_TYPES = ["Lung", "Breast", "Colon", "Prostate", "Blood"]
PRIORITY_LEVELS = ["Normal", "Urgent"]
RESOURCES_BY_DEPARTMENT = {
    "Referral Office": ["Admin A", "Admin B"],
    "Oncology": ["Dr. Chen", "Dr. Patel", "Dr. Smith"],
    "Radiology": ["Tech A", "Tech B"],
    "Pathology": ["Pathologist A", "Pathologist B"],
    "Treatment Unit": ["Nurse A", "Nurse B", "Nurse C"],
}


def random_delay_days(activity_name: str, priority_level: str, cancer_type: str) -> int:
    base_ranges = {
        "Referral Received": (0, 1),
        "Intake Review": (1, 3),
        "Initial Consultation": (2, 5),
        "Diagnostic Imaging": (3, 10),
        "Diagnosis Confirmed": (2, 7),
        "Treatment Planning": (2, 5),
        "Treatment Start": (4, 12),
        "Follow-Up": (14, 30),
    }

    low, high = base_ranges[activity_name]
    delay = random.randint(low, high)

    if priority_level == "Urgent":
        delay = max(low, delay - 2)

    if activity_name == "Diagnostic Imaging" and cancer_type == "Lung":
        delay += random.randint(1, 4)

    if activity_name == "Treatment Start" and cancer_type in {"Colon", "Breast", "Blood"}:
        delay += random.randint(1, 3)

    return delay


def maybe_skip_activity(activity_name: str) -> bool:
    skip_chance = {
        "Follow-Up": 0.08,
    }
    return random.random() < skip_chance.get(activity_name, 0.0)


def create_event_log(num_cases: int = 200) -> pd.DataFrame:
    rows = []
    start_date = datetime(2025, 1, 1, 8, 0, 0)

    for i in range(1, num_cases + 1):
        case_id = f"C{i:04d}"
        cancer_type = random.choice(CANCER_TYPES)
        priority_level = random.choices(PRIORITY_LEVELS, weights=[0.75, 0.25], k=1)[0]

        current_time = start_date + timedelta(days=random.randint(0, 45))

        for activity_name, department in ACTIVITY_FLOW:
            if maybe_skip_activity(activity_name):
                continue

            delay_days = random_delay_days(activity_name, priority_level, cancer_type)
            current_time += timedelta(
                days=delay_days,
                hours=random.randint(0, 7),
                minutes=random.randint(0, 59),
            )

            rows.append(
                {
                    "case_id": case_id,
                    "activity": activity_name,
                    "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "cancer_type": cancer_type,
                    "priority_level": priority_level,
                    "department": department,
                    "resource": random.choice(RESOURCES_BY_DEPARTMENT[department]),
                }
            )

    df = pd.DataFrame(rows)
    df = df.sort_values(by=["case_id", "timestamp"]).reset_index(drop=True)
    return df


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = create_event_log(num_cases=200)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Created raw event log: {OUTPUT_PATH}")
    print(f"Rows: {len(df)}")
    print(f"Cases: {df['case_id'].nunique()}")
    print("\nSample:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()