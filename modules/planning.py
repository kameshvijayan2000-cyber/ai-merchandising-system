import streamlit as st
import pandas as pd
import os
from datetime import date

FILE = "data/production_detailed.csv"

def run():

    st.header("📊 Production Tracking (Advanced)")

    # ✅ CHECK COUNT CALCULATOR DATA
    if "order_detail" not in st.session_state:
        st.warning("⚠️ Please calculate order in Count Calculator first")
        return

    order_df = st.session_state["order_detail"]

    # ---------- SHOW TARGET ----------
    st.subheader("🎯 Target Plan")
    st.dataframe(order_df, use_container_width=True)

    # ---------- FILE SETUP ----------
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Date", "Process", "Color", "Size", "Qty"
        ])
        df.to_csv(FILE, index=False)

    df = pd.read_csv(FILE)

    # ---------- INPUT ----------
    st.subheader("➕ Enter Production")

    entry_date = st.date_input("Date", value=date.today())
    process = st.text_input("Process (Cutting / Stitching / etc)")

    color_list = order_df["Color"].unique().tolist()
    size_list = order_df["Size"].unique().tolist()

    selected_color = st.selectbox("Select Color", color_list)
    selected_size = st.selectbox("Select Size", size_list)

    qty = st.number_input("Produced Quantity", min_value=0)

    if st.button("Save Entry"):

        new = pd.DataFrame([[entry_date, process, selected_color, selected_size, qty]],
                           columns=df.columns)

        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)

        st.success("✅ Production Saved")

    # ---------- LOG ----------
    st.subheader("📋 Production Log")
    st.dataframe(df, use_container_width=True)

    # ---------- PROCESS FILTER (🔥 MAIN FIX) ----------
    st.subheader("📈 Size-wise Progress")

    if not df.empty:

        process_list = df["Process"].unique().tolist()
        selected_process = st.selectbox("Select Process to View", process_list)

        # FILTER ONLY SELECTED PROCESS
        filtered_df = df[df["Process"] == selected_process]

        produced_df = filtered_df.groupby(["Color", "Size"])["Qty"].sum().reset_index()

        merged = pd.merge(
            order_df,
            produced_df,
            on=["Color", "Size"],
            how="left"
        )

        merged["Qty"] = merged["Qty"].fillna(0)
        merged["Pending"] = merged["Quantity"] - merged["Qty"]

        merged.rename(columns={
            "Quantity": "Target",
            "Qty": "Produced"
        }, inplace=True)

        st.dataframe(merged, use_container_width=True)

        # ---------- TOTALS (FOR SELECTED PROCESS ONLY) ----------
        total_target = merged["Target"].sum()
        total_done = merged["Produced"].sum()
        total_pending = merged["Pending"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("🎯 Total Target", int(total_target))
        col2.metric("✅ Produced", int(total_done))
        col3.metric("⏳ Pending", int(total_pending))

    # ---------- PROCESS SUMMARY ----------
    st.subheader("📊 Process-wise Production")

    if not df.empty:
        process_summary = df.groupby("Process")["Qty"].sum().reset_index()
        st.dataframe(process_summary, use_container_width=True)

    # ---------- DELETE ----------
    st.subheader("🗑️ Delete Entry")

    if len(df) > 0:
        index = st.number_input("Row Number", 0, len(df)-1, 0)

        if st.button("Delete Row"):
            df = df.drop(index).reset_index(drop=True)
            df.to_csv(FILE, index=False)
            st.success("Row deleted")

    # ---------- CLEAR ----------
    if st.button("🗑️ Clear All Data"):
        df = pd.DataFrame(columns=df.columns)
        df.to_csv(FILE, index=False)
        st.warning("All data cleared")
