
🌐 Ozone Level Forecasting & Air Quality Visualization System

 📌 Project Overview
This project presents a comprehensive **Ozone Prediction and Air Quality Analysis System** designed to forecast future ozone concentration levels across multiple locations in Bangalore using historical air quality data and deep learning techniques.
By leveraging **LSTM (Long Short-Term Memory) neural networks**, the system is capable of predicting monthly ozone levels up to **four years into the future**, assisting in proactive air quality management and public health awareness.
The project also includes rich **graphical visualizations** to analyze pollutant relationships, seasonal trends, and time-series patterns at selected monitoring stations.
### 🧪 Features

* ✅ Ozone Level Forecasting** (2024–2027) per location.
* ✅ Pollutant Comparison & Correlation Analysis** (Ozone vs NOx, PM2.5, etc.).
* ✅ Interactive Visualizations** via Streamlit:

  * Time-series plots
  * Pollution relationship scatter plots
* ✅ Supports 7 key air quality stations**:

  * Bapujinagar
  * Jayanagar
  * Silk Board
  * BTM Layout
  * Peenya
  * RVCE Campus
  * Kasturba Road

---

### 🧰 Technologies Used

| Component       | Technology/Library           |
| --------------- | ---------------------------- |
| Data Processing | `Pandas`, `NumPy`            |
| Modeling        | `TensorFlow`, `Keras` (LSTM) |
| Visualization   | `Matplotlib`, `Seaborn`      |
| Interface (UI)  | `Streamlit`                  |
| File Format     | `.csv` (input data)          |

---

### 📂 Project Structure

```
📁 ozone-predictor/
├── main.py                 # Streamlit dashboard and logic
├── predictor.py            # LSTM-based prediction model
├── /data/                  # 7 cleaned station CSV files
│   ├── jayanagar_fixed.csv
│   ├── silkboard_fixed.csv
│   └── ...
├── README.md               # Project description
└── requirements.txt        # Python dependencies
```

#####

###


🔗 Getting Started

1. Clone the repository
2. Install the libraries by - pip install pandas numpy seaborn matplotlib scikit-learn tensorflow pillow streamlit
3. Place the `.csv` files in the `data/` folder
4. Run the Streamlit app using:

   ```bash
   streamlit run main.py
   ```



