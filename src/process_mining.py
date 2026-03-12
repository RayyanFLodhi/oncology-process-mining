from pathlib import Path
import pandas as pd
import pm4py

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EVENT_LOG_PATH = PROJECT_ROOT / "data" / "pm4py_event_log.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

PROCESS_MAP_FILE = OUTPUT_DIR / "process_map.png"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(EVENT_LOG_PATH)
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])

    print("Running process discovery...")

    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(
        df,
        case_id_key="case:concept:name",
        activity_key="concept:name",
        timestamp_key="time:timestamp",
    )

    gviz = pm4py.visualization.petri_net.visualizer.apply(
        net, initial_marking, final_marking
    )

    pm4py.visualization.petri_net.visualizer.save(gviz, str(PROCESS_MAP_FILE))

    print(f"\nProcess map saved to: {PROCESS_MAP_FILE}")

    print("\nActivity Frequency:")
    print(df["concept:name"].value_counts())

    case_counts = df.groupby("case:concept:name").size()
    print("\nAverage events per case:", round(case_counts.mean(), 2))
    print("Max events in a case:", int(case_counts.max()))


if __name__ == "__main__":
    main()