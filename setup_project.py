from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

folders = [
    "data",
    "db",
    "src",
    "outputs",
    "powerbi",
]

files = {
    "README.md": """# Oncology Process Mining

A small MVP project that simulates oncology patient event logs, stores them in SQLite, transforms them with Python, applies PM4Py for process mining, and visualizes bottlenecks in Power BI.
""",

    "requirements.txt": """pandas
pm4py
matplotlib
""",

    "db/schema.sql": """CREATE TABLE IF NOT EXISTS event_log (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id TEXT NOT NULL,
    activity TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    cancer_type TEXT,
    priority_level TEXT,
    department TEXT,
    resource TEXT
);
""",

    "src/generate_data.py": """# TODO: Generate synthetic oncology patient event logs
print("generate_data.py is ready.")
""",

    "src/load_to_sqlite.py": """# TODO: Load CSV event log into SQLite
print("load_to_sqlite.py is ready.")
""",

    "src/transform_event_log.py": """# TODO: Clean and sort event log for PM4Py
print("transform_event_log.py is ready.")
""",

    "src/process_mining.py": """# TODO: Run PM4Py process discovery
print("process_mining.py is ready.")
""",

    "src/export_for_powerbi.py": """# TODO: Export summary tables for Power BI
print("export_for_powerbi.py is ready.")
""",
}

def main() -> None:
    for folder in folders:
        (PROJECT_ROOT / folder).mkdir(parents=True, exist_ok=True)

    for relative_path, content in files.items():
        file_path = PROJECT_ROOT / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")
            print(f"Created: {file_path.relative_to(PROJECT_ROOT)}")
        else:
            print(f"Skipped existing file: {file_path.relative_to(PROJECT_ROOT)}")

    print("\\nProject scaffold complete.")

if __name__ == "__main__":
    main()