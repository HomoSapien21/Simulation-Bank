import math
import pandas as pd
import numpy as np
import streamlit as st
import os

# Import functions from your `fig_func` module
# Replace with actual imports or implementations
from modules.fig_func import (
    plot_gantt_chart, entVsWT, entVsTA, entVsArrival, entVsService, ServerUtilization, calculate_server_utilization
)

# Function to calculate cumulative probability
def calculate_CP(x, lambda_rate, prev_cp):
    return prev_cp + (math.exp(-lambda_rate) * (lambda_rate ** x) / math.factorial(x))

# Function to calculate service time
def calculate_service_time(mu_rate):
    return math.ceil(-mu_rate * np.log(np.random.rand()))

# Main M/M/n simulation function
def mmn(lambda_rate, mu_rate, num_entries, num_servers):
    service_times = []
    cp_values = []
    inter_arrival_times = [0]
    arrival_times = [0]
    turn_around_times = []
    wait_times = []
    response_times = []

    prev_cp = 0
    customers = [f"{i}" for i in range(num_entries)]

    for i in range(num_entries):
        cp = calculate_CP(i, lambda_rate, prev_cp)
        prev_cp = cp
        cp_values.append(cp)
        service_times.append(calculate_service_time(mu_rate))

    cp_values.append(1)  # Ensure cumulative probability ends at 1
    labels = [f"{0.0000}-{cp_values[0]:.4f}"] + [
        f"{cp_values[i]:.4f}-{cp_values[i + 1]:.4f}" for i in range(len(cp_values) - 1)
    ]

    df = pd.DataFrame({"Customer": customers, "Cumulative Probability": cp_values[0:num_entries]})
    df['I.A Range'] = labels[0:num_entries]

    arrival = 0
    for i in range(num_entries - 1):
        random = np.random.random()
        for j in range(len(df['Cumulative Probability'])):
            if random < df['Cumulative Probability'][j]:
                inter_arrival_times.append(j)
                arrival += j
                arrival_times.append(arrival)
                break

    df["Inter Arrival Time"] = inter_arrival_times
    df["Arrival Time"] = arrival_times
    df["Service Time"] = service_times

    # Assign servers and calculate times
    servers = [0] * num_servers
    start_times = []

    for i in range(len(df)):
        server = servers.index(min(servers))
        assigned_start_time = max(df.loc[i, "Arrival Time"], servers[server])
        servers[server] = assigned_start_time + df.loc[i, "Service Time"]

        df.loc[i, "Server"] = server
        start_times.append(assigned_start_time)

    df["Start Time"] = start_times
    df["End Time"] = df["Start Time"] + df["Service Time"]

    # Calculate performance metrics
    for i, row in df.iterrows():
        turn_around = row["End Time"] - row["Arrival Time"]
        wait = turn_around - row["Service Time"]
        response = row["Start Time"] - row["Arrival Time"]

        turn_around_times.append(turn_around)
        wait_times.append(wait)
        response_times.append(response)

    df["Turn Around Time"] = turn_around_times
    df["Response Time"] = response_times
    df["Wait Time"] = wait_times

    return df

# Streamlit application
st.title("Simulation Of Bank Data")

# Load data
try:
    data_path = "./data/Goodness Of Fit Test(ChiSquare).xlsx"
    if not os.path.exists(data_path):
        st.error("Data file not found. Please ensure the file exists at './data/Goodness Of Fit Test(ChiSquare).xlsx'.")
    else:
        data = pd.read_excel(data_path, sheet_name="Sheet1")
        st.success("Data loaded successfully.")

        # Calculate lambda and mu rates
        if len(data["INTER-ARRIVAL TIME(MIN)"].dropna()) > 90 and len(data["SERVICE TIME (MIN)"].dropna()) > 90:
            lambda_rate = 1 / data["INTER-ARRIVAL TIME(MIN)"].dropna().iloc[90]
            mu_rate = 1 / data["SERVICE TIME (MIN)"].dropna().iloc[90]
        else:
            st.error("Insufficient data to calculate λ and μ. Ensure at least 91 rows in the dataset.")
except Exception as e:
    st.error(f"An error occurred while loading data: {str(e)}")

# Simulation
if st.button("Generate Simulation"):
    try:
        df = mmn(lambda_rate, mu_rate, num_entries=90, num_servers=3)
        st.write("### Simulation Results")
        # st.dataframe(df, hide_index=True)

        # Calculate averages
        avg_interarrival = df["Inter Arrival Time"].mean()
        avg_service = df["Service Time"].mean()
        avg_TA = df["Turn Around Time"].mean()
        avg_WT = df["Wait Time"].mean()
        avg_RT = df["Response Time"].mean()

        st.write(f"**Average Inter-Arrival Time**: {avg_interarrival:.2f}")
        st.write(f"**Average Service Time**: {avg_service:.2f}")
        st.write(f"**Average Turn-Around Time**: {avg_TA:.2f}")
        st.write(f"**Average Wait Time**: {avg_WT:.2f}")
        st.write(f"**Average Response Time**: {avg_RT:.2f}")

        # Plots and charts
        st.write("### Gantt Chart for Servers")
        plot_gantt_chart(df,num_servers=3)

        st.write("### Wait Time vs Customers")
        entVsWT(df["Customer"], df["Wait Time"])

        st.write("### Turnaround Time vs Customers")
        entVsTA(df["Customer"], df["Turn Around Time"])

        st.write("### Arrival Time vs Customers")
        entVsArrival(df["Customer"], df["Arrival Time"])

        st.write("### Service Time vs Customers")
        entVsService(df["Customer"], df["Service Time"])

        st.write("### Server Utilization")
        server_util = calculate_server_utilization(df)
        for server, utilization in server_util.items():
            ServerUtilization(utilization)
    except Exception as e:
        st.error(f"An error occurred during the simulation: {str(e)}")
