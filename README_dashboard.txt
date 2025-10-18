# Dashboard Setup Guide

## Overview
This dashboard visualizes live traffic data stored in the MySQL database (`raw_data_kafka`) using **Highcharts**.  
It automatically updates every few seconds and allows users to pause/resume updates interactively.

---

## Requirements

**Install the following:**
- Python 3.9+  
- MySQL database (already populated with `raw_data_kafka` table)  
- Flask and Flask-CORS libraries  
- Web browser (Chrome recommended)

---

## Project Structure
```
C:\Capstone\highcharts
│
├── app.py             # Flask API serving MySQL data as JSON
├── dashboard.html     # Highcharts frontend dashboard
└── README_dashboard.txt
```

---

## Step 1 — Install Dependencies

Open a terminal and run:
python -m pip install flask
pip install flask-cors

---

## Step 2 — Start the Flask API

From inside the project folder:
```
cd C:\Capstone\highcharts
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000/
```

Test it in your browser:
http://127.0.0.1:5000/data

If you see JSON output, the backend is working.

---

## Step 3 — Launch the Dashboard

Run a quick local server:
```bash
python -m http.server 5500
```

Then visit:
http://127.0.0.1:5500/dashboard.html