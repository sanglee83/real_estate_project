import streamlit as st
import pandas as pd
import pickle
import os
import plotly.graph_objects as go

# Streamlit page setup
st.set_page_config(page_title="Pickle Data Viewer", layout="wide")
st.title("Pickle Data Viewer with Fishbone and Box Plot")
st.markdown("This page filters data where `area2` is between 80 and 100 and `tradeTypeName` is '매매', and overlays a box plot on the fishbone plot for `articleConfirmYmd` vs `dealOrWarrantPrc`.")

# Pickle 파일 경로
pickle_file = "real_estate_data.pkl"

# Function to load pickle data
def load_pickle_data(pickle_file):
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as f:
            data = pickle.load(f)
        return pd.DataFrame(data)  # Return as DataFrame for easy viewing
    else:
        return None

# Function to convert "23억" to numerical value
def convert_price_to_number(price_str):
    if isinstance(price_str, str):
        if "억" in price_str:
            try:
                return float(price_str.replace("억", "").replace(",", "").strip()) * 1e8
            except ValueError:
                return None
    return price_str

# Load data from pickle file
data = load_pickle_data(pickle_file)

if data is not None and not data.empty:
    # Convert dealOrWarrantPrc from "23억" to numeric values
    data["dealOrWarrantPrc"] = data["dealOrWarrantPrc"].apply(convert_price_to_number)

    # Filter data: `area2` between 80 and 100 and `tradeTypeName` == "매매"
    filtered_data = data[(data["area2"] >= 80) & (data["area2"] <= 100) & (data["tradeTypeName"] == "매매")]

    # Ensure `articleConfirmYmd` is in datetime format
    filtered_data["articleConfirmYmd"] = pd.to_datetime(filtered_data["articleConfirmYmd"], errors="coerce")
    filtered_data = filtered_data.dropna(subset=["articleConfirmYmd", "dealOrWarrantPrc"])  # Drop rows with missing values

    # Sort data by date for better visualization
    filtered_data = filtered_data.sort_values(by="articleConfirmYmd")

    # Create a fishbone plot with Plotly
    fishbone_fig = go.Figure()

    # Add Fishbone (Strip Plot)
    fishbone_fig.add_trace(
        go.Scatter(
            x=filtered_data["articleConfirmYmd"],
            y=filtered_data["dealOrWarrantPrc"],
            mode="markers",
            name="Fishbone",
            marker=dict(size=8, color="orange", opacity=0.7),
        )
    )

    # Add Box Plot
    fishbone_fig.add_trace(
        go.Box(
            x=filtered_data["articleConfirmYmd"],
            y=filtered_data["dealOrWarrantPrc"],
            name="Box Plot",
            marker=dict(color="blue"),
            boxmean=True,  # Add mean indicator
        )
    )

    # Customize y-axis to display "억" format
    def format_to_oku(value):
        return f"{value / 1e8:.0f}억"

    y_ticks = filtered_data["dealOrWarrantPrc"].unique()
    y_ticks.sort()

    fishbone_fig.update_layout(
        title="Fishbone and Box Plot of Deal Price Over Time (Filtered by Area2: 80-100 and TradeTypeName: '매매')",
        xaxis_title="Article Confirm Date",
        yaxis_title="Deal or Warrant Price",
        title_x=0.5,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        yaxis=dict(
            tickvals=y_ticks,
            ticktext=[format_to_oku(value) for value in y_ticks],
        )
    )

    # Display the combined plot
    st.plotly_chart(fishbone_fig, use_container_width=True)

    # Sort filtered data by date in descending order for display
    filtered_data = filtered_data.sort_values(by="articleConfirmYmd", ascending=False)

    # Convert numerical prices back to "억" format for display
    filtered_data["dealOrWarrantPrc"] = filtered_data["dealOrWarrantPrc"].apply(lambda x: f"{x / 1e8:.0f}억")

    # Display the filtered data below the plot
    st.write("### Filtered Data (Area2 between 80 and 100, TradeTypeName: '매매')")
    st.dataframe(filtered_data)
else:
    st.write("No data found in the pickle file or data does not meet the criteria.")
