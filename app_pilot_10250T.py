import streamlit as st
import pandas as pd
from itertools import product

# Load data
@st.cache_data
def load_data():
    operator_df = pd.read_csv("NonIlluminatedPushbuttonOperator.csv", header=None, names=["Operator Type", "Code"])
    color_df = pd.read_csv("NonIlluminatedPushbuttonButtonColor.csv", header=None, names=["Color", "Code"])
    circuit_df = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None, names=["Circuit Type", "Code"])
    
    # Drop header rows that were read as data
    operator_df = operator_df[1:].reset_index(drop=True)
    color_df = color_df[1:].reset_index(drop=True)
    circuit_df = circuit_df[1:].reset_index(drop=True)
    
    return operator_df, color_df, circuit_df

operator_df, color_df, circuit_df = load_data()

# UI
st.title("10250T Non-Illuminated Pushbutton Configurator")

st.markdown("Select specifications to generate a catalog number:")

operator_choice = st.selectbox("Operator Type", operator_df["Operator Type"].tolist())
color_choice = st.selectbox("Button Color", color_df["Color"].tolist())
circuit_choice = st.selectbox("Circuit Type", circuit_df["Circuit Type"].tolist())

# Get corresponding codes
op_code = operator_df[operator_df["Operator Type"] == operator_choice]["Code"].values[0]
color_code = color_df[color_df["Color"] == color_choice]["Code"].values[0]
circuit_code = circuit_df[circuit_df["Circuit Type"] == circuit_choice]["Code"].values[0]

# Generate catalog number
catalog_number = f"10250T{op_code}{color_code}-{circuit_code}"

st.markdown("### Generated Catalog Number")
st.code(catalog_number)

# Optionally show all combinations
if st.checkbox("Show all possible combinations"):
    combinations = list(product(operator_df["Code"], color_df["Code"], circuit_df["Code"]))
    all_catalogs = [f"10250T{op}{col}-{cir}" for op, col, cir in combinations]
    st.write(f"Total combinations: {len(all_catalogs)}")
    st.dataframe(pd.DataFrame(all_catalogs, columns=["Catalog Number"]))
