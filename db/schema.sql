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
