import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from predictor import predict_future

st.set_page_config(page_title="Ozone Predictor", layout="wide")

# Location-to-file mapping
location_map = {
    "Bapujinagar": "C:/Users/Radha/OneDrive/Desktop/OZONE/bapujinagar_cleaned_final.csv",
    "Jaynagar": "C:/Users/Radha/OneDrive/Desktop/OZONE/jayanagar_fixed.csv",
    "Silk Board": "C:/Users/Radha/OneDrive/Desktop/OZONE/silkboard_fixed.csv",
    "BTM": "C:/Users/Radha/OneDrive/Desktop/OZONE/btm_fixed.csv",
    "Peenya": "C:/Users/Radha/OneDrive/Desktop/OZONE/peenya_fixed.csv",
    "RVCE": "C:/Users/Radha/OneDrive/Desktop/OZONE/rvce_fixed.csv",
    "Kasturba": "C:/Users/Radha/OneDrive/Desktop/OZONE/kasturba_fixed.csv",
}

# Sidebar mode switch
mode = st.sidebar.radio("Select Mode", ["Prediction", "Graphs & Visualization"])

# PREDICTION MODE

if mode == "Prediction":
    st.title("Ozone Level Prediction")

    location = st.selectbox("Select Location", list(location_map.keys()))
    selected_years = st.multiselect("Select Year(s) to Predict", [2024, 2025, 2026, 2027])

    if st.button("Generate Prediction"):
        if not selected_years:
            st.warning("Please select at least one year to predict.")
        else:
            file_path = location_map[location]
            results = {}

            for year in selected_years:
                predictions = predict_future(file_path, year)
                avg_ozone = round(predictions.mean(), 2)
                results[year] = avg_ozone

            # Display table
            result_df = pd.DataFrame(list(results.items()), columns=["Year", "Predicted Avg Ozone Level"])
            st.dataframe(result_df.set_index("Year"))

            # Plot trend
            fig, ax = plt.subplots()
            ax.plot(result_df["Year"], result_df["Predicted Avg Ozone Level"], marker='o')
            ax.set_title(f"Predicted Ozone Level Trend in {location}")
            ax.set_xlabel("Year")
            ax.set_ylabel("Average Ozone Level (µg/m³)")
            st.pyplot(fig)


# 📊 VISUALIZATION MODE

elif mode == "Graphs & Visualization":
    st.title("Air Quality Visualization")

    station_name = st.selectbox("Choose Station for Analysis", list(location_map.keys()))

    try:
        df = pd.read_csv(location_map[station_name], parse_dates=['date'])
    except ValueError:
        st.error("The selected dataset does not contain a 'date' column. Please check the CSV file.")
        st.stop()

    tab1, tab2, tab3 = st.tabs([
        "Pollutant Comparisons",
        "Pollutant Relationship",
        "Time Series Analysis"

    ])

    # Tab 1: Ozone vs Selected Pollutant (Comparison)
    with tab1:
        st.header("Compare Ozone with Other Pollutants")

        ozone_col = next((col for col in df.columns if 'ozone' in col.lower()), None)

        if ozone_col:
            other_pollutants = [col for col in df.columns if col != ozone_col and col.lower() != 'date']
            selected_pollutant = st.selectbox("Select a pollutant to compare with Ozone", other_pollutants)

            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=ozone_col, y=selected_pollutant, ax=ax)
            ax.set_title(f"{ozone_col} vs {selected_pollutant}")
            ax.set_xlabel("Ozone (µg/m³)")
            ax.set_ylabel(f"{selected_pollutant}")
            st.pyplot(fig)
        else:
            st.warning("Ozone column not found in dataset.")

    # Tab 2: Any Pollutant vs Any Pollutant
    with tab2:
        st.header("Relationship Between Two Pollutants")
        pollutant_columns = [col for col in df.columns if col.lower() != 'date']

        col1, col2 = st.columns(2)
        with col1:
            x_pollutant = st.selectbox("Select First Pollutant", pollutant_columns, key="x_pollutant")
        with col2:
            y_pollutant = st.selectbox("Select Second Pollutant", pollutant_columns, key="y_pollutant")

        st.subheader(f"Relationship Between {x_pollutant} and {y_pollutant}")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=x_pollutant, y=y_pollutant, ax=ax)
        ax.set_title(f"{x_pollutant} vs {y_pollutant} at {station_name}")
        st.pyplot(fig)

    # Time Series Analysis
    with tab3:
        st.header("Time Series Analysis")

        col1, col2 = st.columns(2)
        with col1:
            selected_location = st.selectbox("Select Location", list(location_map.keys()), key="ts_location")
        with col2:
            time_agg = st.selectbox("Select Time Aggregation", ["Daily", "Weekly", "Monthly"], key="time_agg")

        df_ts = pd.read_csv(location_map[selected_location])
        if 'date' not in df_ts.columns:
            st.warning("No 'date' column found in dataset.")
        else:
            df_ts['date'] = pd.to_datetime(df_ts['date'], errors='coerce')
            df_ts = df_ts.dropna(subset=['date'])

            pollutant_cols = [col for col in df_ts.columns if col != 'date']
            pollutant = st.selectbox("Select Pollutant", pollutant_cols, key="pollutant_ts")

            df_ts.set_index('date', inplace=True)

            if time_agg == "Weekly":
                df_plot = df_ts[[pollutant]].resample('W').mean()
            elif time_agg == "Monthly":
                df_plot = df_ts[[pollutant]].resample('M').mean()
            else:
                df_plot = df_ts[[pollutant]]

            st.subheader(f"{pollutant} Levels Over Time ({time_agg}) at {selected_location}")
            fig, ax = plt.subplots()
            df_plot.plot(ax=ax)
            ax.set_ylabel(pollutant)
            st.pyplot(fig)





