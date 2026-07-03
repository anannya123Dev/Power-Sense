# ⚡ PowerSense — Real-Time Power Monitoring System

A machine learning powered electricity monitoring dashboard built
with Flask, SQLite, and Random Forest. Runs fully on synthetic
data out of the box — no hardware needed.

## 📸 What you'll see

- Live dashboard with real-time power readings (updates every 5s)
- ML prediction of total power consumption
- Low / Medium / High classification
- Device-wise consumption with toggles
- Bill estimator
- Historical data with charts and date filters
- Beginner-friendly guide page

## ⚙️ Setup — runs in under 2 minutes

### 1. Clone the repo
git clone https://github.com/yourname/powersense.git
cd powersense

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the app
python app.py

### 4. Open your browser
http://127.0.0.1:5000

That's it. No API keys, no hardware, no configuration needed.
The app generates synthetic sensor data automatically.

## 🧠 How it works

| Component        | Technology              |
|------------------|-------------------------|
| Web framework    | Flask (Python)          |
| ML model         | Random Forest (sklearn) |
| Database         | SQLite                  |
| Frontend charts  | Chart.js                |
| Fonts            | Google Fonts            |
| Data source      | Synthetic (simulated)   |

## 📁 Project structure

| File                  | Purpose                              |
|-----------------------|--------------------------------------|
| app.py                | Flask routes and background loop     |
| data_collector.py     | Generates synthetic sensor data      |
| preprocessing.py      | Cleaning and hybrid power calc       |
| ml_model.py           | Train and predict with Random Forest |
| database.py           | SQLite read/write operations         |
| bill_calculator.py    | kWh and cost estimation              |
| templates/index.html  | Live dashboard                       |
| templates/history.html| Historical data and charts           |
| templates/guide.html  | Beginner-friendly explainer          |

## 🔌 Want to connect real hardware?

Replace `get_api_data()` in `data_collector.py` with real
Shelly smart plug API calls. Everything else works unchanged.

## 📊 ML Model

- Algorithm: Random Forest Regressor (100 trees)
- Features: Voltage, Current, Hybrid Power
- Target: Total Power Consumption (W)
- Classification: Low (<500W) / Medium (<1500W) / High (>1500W)
- Model auto-trains on first run using synthetic data
