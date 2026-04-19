import streamlit as st
import pandas as pd
import os
from datetime import date

ORDER_FILE = "data/order_details.csv"
TRACK_FILE = "data/production_detailed.csv"

def run():

    st.header("📊 Production Tracking (Advanced)")

    # ---------- LOAD ORDER ----------
    if not os.path.exists(ORDER_FILE):
        st.warning("⚠️ Run Count Calculator first")
        return

    order_df = pd.read_csv(ORDER_FILE)

    st.subheader("🎯 Target Plan")
    st.dataframe(order_df, use_container_width=True)

    # ---------- FILE SETUP ----------
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(TRACK_FILE):
        df = pd.DataFrame(columns=["Date", "Process", "Color", "Size", "Qty"])
        df.to_csv(TRACK_FILE, index=False)

    df = pd.read_csv(TRACK_FILE)

    # ---------- INPUT ----------
    st.subheader("➕ Enter Production")

    entry_date = st.date_input("Date", value=date.today())
    process = st.text_input("Process")

    color_list = order_df["Color"].unique().tolist()
    size_list = order_df["Size"].unique().tolist()

    selected_color = st.selectbox("Color", color_list)
    selected_size = st.selectbox("Size", size_list)

    qty = st.number_input("Produced Qty", 0)

    if st.button("Save Entry"):

        new = pd.DataFrame([[entry_date, process, selected_color, selected_size, qty]],
                           columns=df.columns)

        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(TRACK_FILE, index=False)

        st.success("Saved")

    # ---------- PROCESS VIEW ----------
    st.subheader("📈 Size-wise Progress")

    if not df.empty:

        process_list = df["Process"].unique().tolist()
        selected_process = st.selectbox("Select Process", process_list)

        filtered_df = df[df["Process"] == selected_process]

        produced_df = filtered_df.groupby(["Color", "Size"])["Qty"].sum().reset_index()

        merged = pd.merge(order_df, produced_df, on=["Color", "Size"], how="left")

        merged["Qty"] = merged["Qty"].fillna(0)
        merged["Pending"] = merged["Quantity"] - merged["Qty"]

        merged.rename(columns={
            "Quantity": "Target",
            "Qty": "Produced"
        }, inplace=True)

        st.dataframe(merged, use_container_width=True)

        st.metric("Total Target", int(merged["Target"].sum()))
        st.metric("Produced", int(merged["Produced"].sum()))
        st.metric("Pending", int(merged["Pending"].sum()))

    # ---------- LOG ----------
    st.subheader("📋 Log")
    st.dataframe(df)

    # ---------- DELETE ----------
    if len(df) > 0:
        idx = st.number_input("Row No", 0, len(df)-1, 0)

        if st.button("Delete"):
            df = df.drop(idx).reset_index(drop=True)
            df.to_csv(TRACK_FILE, index=False)
            st.success("Deleted")
