import streamlit as st

def run():
    st.header("📊 Production Planning")

    order_qty = st.number_input("Order Qty", value=5000)
    consumption = st.number_input("Consumption", value=0.55)
    wastage = st.number_input("Wastage %", value=8.0)
    available = st.number_input("Available Fabric (kg)", value=2800)

    required = order_qty * consumption * (1 + wastage / 100)
    balance = available - required

    st.metric("Required Fabric", f"{round(required, 2)} kg")

    if balance >= 0:
        st.success(f"Excess: {round(balance, 2)} kg")
    else:
        st.error(f"Shortage: {abs(round(balance, 2))} kg")
