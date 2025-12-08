import numpy as np
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Simulator", 
    page_icon="./data/simulation.png",  
    layout="centered",  
    initial_sidebar_state="auto" 
)

st.title("Welcome to the Simulation Project (HBL BANK)")
st.subheader("Group Members:")
st.write("1. Mohammad Ahmed - B21110006058")
st.write("2. Qaim Hassan - B21110006105")
st.write("3. Muntazir Hassan - B21110006100")
st.write("4. Syed Shahamuddin Shameer - B2110006138")
st.write("5. Abdul Moiz - B2110006002")
st.write(" ")
st.title("1-Data")

df = pd.read_excel("./data/Goodness Of Fit Test(ChiSquare).xlsx")

# Fill missing values with "-"
df.fillna("-", inplace=True)


data = df.iloc[:90]  # Use .iloc[:94] for integer-based indexing

# Extract specific columns by their names
columns_to_display = [
    "CUSTOMER", 
    "ARRIVAL TIME ", 
    "SERVICE TIME(START)", 
    "SERVICE TIME(END)", 
    "INTER-ARRIVAL TIME(MIN)", 
    "SERVICE TIME (MIN)"
]

# Filter the DataFrame to include only the specified columns
filtered_data = data[columns_to_display]

# Display the filtered DataFrame in Streamlit without an index
# st.dataframe(filtered_data, hide_index=True)
st.dataframe(filtered_data, width=1000, height=300, hide_index=True)

st.title("2-Chi square test")
st.subheader("i)GOODNESS OF FITNESS INTER-ARRIVAL")
header = df.iloc[94]  # This is the row you want to set as the header


# Create a new DataFrame with the row as the column names
IA_chiSquare = df.iloc[95:104].fillna("-")  # Data starting from row 95 to 104
IA_chiSquare.columns = header  # Set the extracted row as column names

# Display the updated DataFrame
# st.dataframe(IA_chiSquare)
st.dataframe(IA_chiSquare, hide_index=True)
st.markdown('<p style="color:green;">Ho is accepted: Inter arrival time for this data is in poisson distribution</p>', unsafe_allow_html=True)

st.subheader("ii)GOODNESS OF FITNESS SERVICE")
Sheader = df.iloc[106]  # This is the row you want to set as the header

# Create a new DataFrame with the row as the column names
S_chiSquare = df.iloc[107:120].fillna(" ")  # Data starting from row 95 to 104
S_chiSquare.columns = header  # Set the extracted row as column names

# Display the updated DataFrame
st.dataframe(S_chiSquare,hide_index=True)

st.markdown('<p style="color:green;">Ho is accepted:Service time for this data is in exponential distribution</p>', unsafe_allow_html=True)









