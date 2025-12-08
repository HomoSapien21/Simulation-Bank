import math
import streamlit as st


st.set_page_config(
    page_title="G/G/S Queuing Calculator", 
    page_icon="./data/simulation.png",  
    layout="centered",  
    initial_sidebar_state="auto" 
)

st.title("G/G/S Queuing Model")

# Function to calculate G/G/S metrics
def GGC(Arrival_Mean, Service_Mean, No_of_server, ArrivalVariance, ServiceVariance):
    lembda = 1 / Arrival_Mean
    meu = 1 / Service_Mean
    c = No_of_server
    p = lembda / (c * meu)  # Utilization factor

    if p >= 1:
        raise ValueError("The system is unstable (utilization factor p >= 1). Please adjust your inputs.")

    Ca = ArrivalVariance / ((1 / lembda) ** 2)  # Coefficient of variation for arrivals
    Cs = ServiceVariance / ((1 / meu) ** 2)  # Coefficient of variation for services

    # Calculating P0
    value = 0
    for m in range(c):
        value += ((c * p) ** m) / math.factorial(m)
    value += ((c * p) ** c) / (math.factorial(c) * (1 - p + 1e-10))  # Add epsilon to avoid division by zero
    Pnot = 1 / value

    # Calculating queue length and waiting times
    Lq = (Pnot * p * (lembda / meu) ** c) / (math.factorial(c) * ((1 - p) ** 2 + 1e-10))  # Add epsilon
    Wq = Lq / lembda
    Wq *= (Ca + Cs) / 2  # Adjusted for variability
    Lq = lembda * Wq
    Ws = Wq + (1 / meu)
    Ls = Ws * lembda

    return Lq, Wq, Ws, Ls, Pnot

# User input fields with default values
Arrival_Mean = st.number_input("Mean Arrival Rate", min_value=0.01, step=0.1, value=1.0, format="%.2f")
Service_Mean = st.number_input("Mean Service Rate", min_value=0.01, step=0.1, value=1.0, format="%.2f")
ArrivalVariance = st.number_input("Arrival Variance", min_value=0.01, step=1.0, value=1.0)
ServiceVariance = st.number_input("Service Variance", min_value=0.01, step=1.0, value=1.0)
No_of_server = st.number_input("Number of Servers", min_value=1, max_value=50, step=1, value=3)

# Button to calculate metrics
if st.button("Calculate Metrics"):
    try:
        Lq, Wq, Ws, Ls, Pnot = GGC(Arrival_Mean, Service_Mean, No_of_server, ArrivalVariance, ServiceVariance)

        # Display results
        st.subheader("Results")
        st.write(f"Queue Length (Lq): {Lq:.2f}")
        st.write(f"Waiting Time in Queue (Wq): {Wq:.2f} hours")
        st.write(f"Total Waiting Time (Ws): {Ws:.2f} hours")
        st.write(f"Total Length of System (Ls): {Ls:.2f}")
        st.write(f"Probability of System Being Empty (P0): {Pnot:.4f}")
    except ValueError as e:
        st.error(str(e))
