import math
import streamlit as st


st.set_page_config(
    page_title="M/G/S Queuing Calculator", 
    page_icon="./data/simulation.png",  
    layout="centered",  
    initial_sidebar_state="auto" 
)


# Functions from your script
def get_normal_statistics(service_mean, service_stddev):
    service_variance = service_stddev ** 2
    return service_mean, service_variance

def get_uniform_statistics(service_min, service_max):
    service_mean = (service_min + service_max) / 2
    service_variance = ((service_max - service_min) ** 2) / 12
    return service_mean, service_variance

def calculate_utilization(arrival_rate, service_rate, num_servers):
    return arrival_rate / (num_servers * service_rate)

def calculate_P0(arrival_rate, service_rate, rho, num_servers):
    try:
        # If service_rate or (1 - rho) is zero, it will raise a ZeroDivisionError
        sum_term = sum([(arrival_rate / service_rate) ** n / math.factorial(n) for n in range(num_servers)])
        P0 = (sum_term + (arrival_rate / service_rate) ** num_servers / math.factorial(num_servers) * 1 / (1 - rho)) ** (-1)
        return P0
    except ZeroDivisionError:
        st.error("Error: Division by zero occurred. Please check the service rate and arrival rate values.")
        return None

def calculate_performance_metrics_variance(arrival_rate, num_servers, distribution, **params):
    if distribution == 'normal':
        service_mean, service_variance = get_normal_statistics(**params)
    elif distribution == "uniform":
        service_mean, service_variance = get_uniform_statistics(**params)
    else:
        st.error("Invalid distribution choice! Please choose either 'normal' or 'uniform'.")
        return

    service_rate = 1 / service_mean
    rho = calculate_utilization(arrival_rate, service_rate, num_servers)
    if rho >= 1:
        return "Error: Utilization (ρ) must be less than 1."
    P0 = calculate_P0(arrival_rate, service_rate, rho, num_servers)
    if P0:
        if num_servers > 1:
            coefficient_of_variation_squared = service_variance / service_mean**2
            Lq = (P0 * ((arrival_rate / service_rate) ** num_servers) / 
                (math.factorial(num_servers) * (1 - rho)**2) * 
                rho * (1 + coefficient_of_variation_squared))
        else:
            Lq = (arrival_rate ** 2 * service_variance) + rho**2 / (2 * (1 - rho))
    
        L = Lq + (arrival_rate / service_rate)
        Wq = Lq / arrival_rate
        W = Wq + (1 / service_rate)
        
        return P0, rho, Lq, L, Wq, W

# Streamlit UI
st.title("M/G/S Queuing Model")

# Input Fields
arrival_rate = st.number_input("Arrival Rate (λ)", min_value=0.01, step=0.01, value=0.1, format="%.2f")


distribution = st.selectbox("Select Service Time Distribution", ["uniform","normal"])

if distribution == "normal":
    # Set reasonable default values that avoid any potential issues
    service_mean = st.number_input("Service Mean (Mean Time)", min_value=0.01, step=0.01, value=1.0, format="%.2f")
    service_stddev = st.number_input("Service Standard Deviation", min_value=0.01, step=0.01, value=0.1, format="%.2f")
    # Ensure service_mean is greater than the service_stddev to avoid negative values in distribution
    if service_mean <= service_stddev:
        st.warning("Service Mean should be greater than Service Standard Deviation for a proper normal distribution.")
    params = {"service_mean": service_mean, "service_stddev": service_stddev}
elif distribution == "uniform":
    service_min = st.number_input("Service Minimum Time", min_value=0.01, step=0.01, value=10.0, format="%.2f")
    service_max = st.number_input("Service Maximum Time", min_value=0.02, step=0.01, value=20.0, format="%.2f")
    params = {"service_min": service_min, "service_max": service_max}


num_servers = st.number_input("Number of Servers (c)", min_value=1, max_value=50, step=1, value=2)
# Calculate and Display Results
if st.button("Calculate Metrics"):
    results = calculate_performance_metrics_variance(arrival_rate, num_servers, distribution, **params)
    if isinstance(results, str):  # Error message
        st.error(results)
    else :
        P0, rho, Lq, L, Wq, W = results
        st.subheader("Results")
        st.write(f"System Utilization (ρ): {rho:.4f}")
        st.write(f"Probability of Idle System (P0): {P0:.4f}")
        st.write(f"Average Queue Length (Lq): {Lq:.4f}")
        st.write(f"Average System Length (L): {L:.4f}")
        st.write(f"Average Waiting Time in Queue (Wq): {Wq:.4f}")
        st.write(f"Average Time in System (W): {W:.4f}")
