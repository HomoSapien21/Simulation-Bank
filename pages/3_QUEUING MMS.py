import math
import streamlit as st

st.set_page_config(
    page_title="M/M/S Queuing Calculator", 
    page_icon="./data/simulation.png",  
    layout="centered",  
    initial_sidebar_state="auto" 
)


st.title("M/M/S Queuing Model")


# Function to calculate M/M/S metrics
def calculate_mms_metrics(arrival, service, servers, rate=False):
    if not rate:
        arrival = 1 / arrival
        service = 1 / service

    rho = arrival / (servers * service)

    # Check for invalid utilization
    if rho >= 1:
        return "Error: Utilization (ρ) must be less than 1."

    # Calculate P0
    first_term = sum([(servers * rho)**n / math.factorial(n) for n in range(servers)])
    second_term = ((servers * rho)**servers / math.factorial(servers)) * (1 / (1 - rho))
    P0 = 1 / (first_term + second_term)

    # Calculate metrics
    Lq = (P0 * ((servers * rho)**servers / math.factorial(servers)) * rho) / ((1 - rho)**2)
    L = Lq + (arrival / service)
    W = L / arrival
    Wq = Lq / arrival

    return rho, P0, Lq, L, W, Wq


# Input fields from the user
input_type = st.radio(
    "Select input type",
    ("Rate", "Mean"),
    index=0,
    horizontal=True
)

# Dynamic input fields for Arrival and Service based on input type
if input_type == "Rate":
    Arrival = st.number_input("Arrival rate (λ)", step=0.1, format="%.2f", min_value=1.0)
    Service = st.number_input("Service rate (μ)", step=0.1, format="%.2f", min_value=1.0)
else:
    Arrival_mean = st.number_input("Mean inter-arrival time (1/λ)", step=0.1, format="%.2f", min_value=1.0)
    Service_mean = st.number_input("Mean service time (1/μ)", step=0.1, format="%.2f", min_value=1.0)

    # Convert mean to rate
    Arrival = 1 / Arrival_mean
    Service = 1 / Service_mean

# Input for the number of servers
No_of_server = st.number_input('Number of servers (c)', min_value=1, max_value=50, step=1)

# Calculate results
if st.button("Calculate Metrics"):
    result = calculate_mms_metrics(Arrival, Service, No_of_server, rate=(input_type == "Rate"))

    # Display results or handle errors
    if isinstance(result, str):  # Error message
        st.error(result)
    else:
        rho, P0, Lq, L, W, Wq = result
        st.subheader("Results:")
        st.write(f"Utilization (ρ): {rho:.2f}")
        st.write(f"Probability of System Being Empty (P0): {P0:.4f}")
        st.write(f"Queue Length (Lq): {Lq:.2f}")
        st.write(f"Length of the System (Ls): {L:.2f}")
        st.write(f"Wait Time in Queue (Wq): {Wq:.2f}")
        st.write(f"Wait Time in System (Ws): {W:.2f}")
