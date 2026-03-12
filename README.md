# Oncology Process Mining Demo

This project demonstrates a simple **process mining pipeline for healthcare workflows**.  
The goal is to simulate oncology treatment event logs, analyze them using **PM4Py**, and visualize operational insights using **Power BI**.

The project was created as a learning exercise to explore **process mining technologies and healthcare process analytics**, similar to those used in clinical workflow monitoring.

---

# Overview

Clinical workflows such as cancer diagnosis and treatment involve multiple sequential stages. Understanding how patients move through these processes can help identify:

- delays in diagnosis
- treatment bottlenecks
- inefficiencies in clinical workflows
- opportunities for operational improvements

This project simulates patient journeys through an oncology treatment pipeline and applies **process mining techniques** to analyze the resulting event logs.

---

# Simulated Oncology Workflow

Each patient case follows a simplified clinical pathway:

Referral Received  
↓  
Intake Review  
↓  
Initial Consultation  
↓  
Diagnostic Imaging  
↓  
Diagnosis Confirmed  
↓  
Treatment Planning  
↓  
Treatment Start  
↓  
Follow-Up  

Each stage generates an **event log entry** containing:

- case ID
- activity name
- timestamp
- cancer type
- department
- priority level

These logs mimic the type of data used in real healthcare process mining systems.

---

# Project Pipeline

The project implements a simple analytics pipeline:

Synthetic Data Generation (Python)  
↓  
Event Log Storage (CSV / SQL ready)  
↓  
Process Discovery (PM4Py)  
↓  
Process Visualization (Graphviz)  
↓  
Business Intelligence Dashboard (Power BI)  

---

# Technologies Used

- Python
- PM4Py – process mining framework
- Pandas – data processing
- Graphviz – process visualization
- Power BI – dashboard and BI analysis
- SQL-ready data exports

---

# Project Structure

oncology-process-mining/

data/  
- synthetic_event_log.csv  
- powerbi_events.csv  
- powerbi_case_summary.csv  
- powerbi_stage_delays.csv  

src/  
- generate_data.py  
- process_mining.py  
- transform_data.py  

outputs/  
- process_map.png  

powerbi/  
- oncology_process_dashboard.pbix  

---

# Example Process Map

Process discovery was performed using the **Inductive Miner algorithm in PM4Py**, producing a Petri net representing the discovered workflow.

Example output workflow:

Referral → Intake → Consultation → Diagnostics → Diagnosis → Treatment → Follow-Up

The discovered model reflects the expected clinical workflow.

---

# Example Insights

Using the generated data we can explore insights such as:

### Case Distribution by Cancer Type

Example visualization in Power BI showing distribution of patient cases across cancer types.

### Average Case Duration

The dashboard calculates the average number of days required for a patient to complete the treatment workflow.

### Stage Delays

Average delays between clinical stages help identify bottlenecks such as:

- imaging delays
- treatment scheduling delays
- diagnosis confirmation lag

---

# Example Output Metrics

Example statistics from the generated dataset:

- **200 simulated patient cases**
- **~8 events per case**
- multiple cancer types simulated
- full end-to-end treatment workflows

---

# How to Run

Install dependencies:

pip install pandas pm4py graphviz

Generate synthetic data:

python src/generate_data.py

Run process mining analysis:

python src/process_mining.py

Outputs will be saved in:

outputs/process_map.png

---

# Power BI Dashboard

The generated CSV files can be imported into Power BI to build a simple operational dashboard.

Example visuals include:

- Total patient cases
- Average case duration
- Case distribution by cancer type
- Stage delay analysis

---

# Purpose

This project was built to explore:

- process mining concepts
- healthcare workflow analytics
- event log analysis
- BI dashboard integration

It demonstrates how **Python analytics pipelines can integrate with business intelligence tools to analyze operational processes**.

---

# Future Improvements

Possible extensions:

- real SQL database integration
- larger synthetic datasets
- conformance checking
- predictive process monitoring
- machine learning on patient flow delays

---

# License

This project is intended for educational and demonstration purposes.