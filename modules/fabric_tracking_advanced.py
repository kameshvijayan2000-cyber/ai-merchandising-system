import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data/fabric_tracking_advanced.csv"

def run():
    st.header("🧵 Fabric Tracking Advanced")

    # ---------- FILE SETUP ----------
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Date", "Style", "Color", "Supplier", "KG"
        ])
        df.to_csv(FILE, index=False)

    df = pd.read_csv(FILE)

    # Fix structure
    expected_cols = ["Date", "Style", "Color", "Supplier", "KG"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    df = df[expected_cols]
    df["KG"] = pd.to_numeric(df["KG"], errors="coerce").fillna(0)

    # ---------- ORDER DETAILS ----------
    st.subheader("📦 Order Details")

    style = st.text_input("Style Name")
    required_fabric = st.number_input("Required Fabric (KG)", value=0.0)

    # ---------- ADD ENTRY ----------
    st.subheader("➕ Add Fabric Entry")

    entry_date = st.date_input("Date", value=date.today())
    color = st.text_input("Color")
    supplier = st.text_input("Supplier / Mill Name")
    kg = st.number_input("Received KG", min_value=0.0)

    if st.button("Add Fabric"):

        if not style or not color:
            st.warning("Enter Style & Color")
        else:
            new = pd.DataFrame([[
                entry_date,
                style,
                color,
                supplier,
                kg
            ]], columns=df.columns)

            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(FILE, index=False)

            st.success("✅ Fabric Added")

    # ---------- DELETE ----------
    st.subheader("🗑️ Delete Entry")

    if len(df) > 0:

        selected_index = st.number_input(
            "Select Row Number",
            min_value=0,
            max_value=len(df) - 1,
            step=1
        )

        if st.button("Delete Row"):
            df = df.drop(index=selected_index).reset_index(drop=True)
            df.to_csv(FILE, index=False)
            st.success("Row deleted")

    # ---------- DISPLAY ----------
    st.subheader("📊 Fabric Entries")
    st.dataframe(df, use_container_width=True)

    # ---------- COLOR SUMMARY ----------
    st.subheader("🎨 Color-wise Summary")

    if not df.empty:

        summary = df.groupby("Color")["KG"].sum().reset_index()
        summary.rename(columns={"KG": "Total KG"}, inplace=True)

        st.dataframe(summary)

    # ---------- TOTAL SUMMARY ----------
    st.subheader("📈 Overall Summary")

    total_received = df["KG"].sum()

    st.metric("Total Fabric Received", f"{round(total_received,2)} KG")

    if required_fabric > 0:
        diff = total_received - required_fabric

        if diff >= 0:
            st.success(f"Excess: {round(diff,2)} KG")
        else:
            st.error(f"Shortage: {abs(round(diff,2))} KG")

    # ---------- CLEAR ----------
    if st.button("🗑️ Clear All Data"):
        df = pd.DataFrame(columns=df.columns)
        df.to_csv(FILE, index=False)
        st.warning("All fabric data cleared!")
