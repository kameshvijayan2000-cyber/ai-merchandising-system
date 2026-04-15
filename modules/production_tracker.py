import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data/production_tracking.csv"

def run():
    st.header("🏭 Production Tracker")

    # ---------- FILE SETUP ----------
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Date", "Process", "Type", "Qty", "Unit", "Party", "Description", "Rate"
        ])
        df.to_csv(FILE, index=False)

    df = pd.read_csv(FILE)

    # ---------- FIX OLD FILE STRUCTURE ----------
    expected_cols = ["Date", "Process", "Type", "Qty", "Unit", "Party", "Description", "Rate"]

    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    df = df[expected_cols]

    # Convert numeric columns
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce").fillna(0)
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce").fillna(0)

    # ---------- INPUT SECTION ----------
    st.subheader("➕ Add Entry")

    processes = [
        "Yarn",
        "Knitting",
        "Dyeing",
        "Compacting",
        "Washing",
        "Fabric Inhouse",
        "Cutting",
        "Stitching",
        "Checking",
        "Ironing",
        "Packing"
    ]

    process = st.selectbox("Select Process", processes)

    custom_process = st.text_input("Or Add Custom Process")
    if custom_process:
        process = custom_process

    entry_type = st.selectbox("Type", ["Input", "Output"])

    entry_date = st.date_input("Date", value=date.today())

    qty = st.number_input("Quantity", min_value=0.0)

    # Unit logic
    if process in ["Cutting", "Stitching", "Checking", "Ironing", "Packing"]:
        unit = "PCS"
    else:
        unit = "KG"

    party = st.text_input("Party / Unit Name")

    # 🔥 NEW FIELDS
    description = st.text_input("Description (Optional)")
    rate = st.number_input("Rate (₹ per unit)", min_value=0.0)

    if st.button("Save Entry"):

        new = pd.DataFrame([[
            entry_date,
            process,
            entry_type,
            qty,
            unit,
            party,
            description,
            rate
        ]], columns=df.columns)

        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)

        st.success("✅ Entry Saved")

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
    st.subheader("📊 All Data")
    st.dataframe(df, use_container_width=True)

    # ---------- SUMMARY ----------
    st.subheader("📈 Stage Summary")

    if not df.empty:

        summary = []

        for p in df["Process"].unique():

            process_df = df[df["Process"] == p]

            input_qty = process_df[process_df["Type"] == "Input"]["Qty"].sum()
            output_qty = process_df[process_df["Type"] == "Output"]["Qty"].sum()

            balance = input_qty - output_qty

            summary.append([
                p,
                round(input_qty, 2),
                round(output_qty, 2),
                round(balance, 2)
            ])

        summary_df = pd.DataFrame(
            summary,
            columns=["Process", "Input", "Output", "Balance"]
        )

        st.dataframe(summary_df)

    # ---------- COST SUMMARY (NEW 🔥) ----------
    st.subheader("💰 Cost Summary")

    df["Total Cost"] = df["Qty"] * df["Rate"]

    cost_summary = df.groupby("Process")["Total Cost"].sum().reset_index()

    st.dataframe(cost_summary)

    st.metric("Total Cost", f"₹ {round(df['Total Cost'].sum(),2)}")

    # ---------- CLEAR ----------
    if st.button("🗑️ Clear All Data"):
        df = pd.DataFrame(columns=df.columns)
        df.to_csv(FILE, index=False)
        st.warning("All tracking data cleared!")
