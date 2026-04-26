import streamlit as st
import pandas as pd
import os
from datetime import date

TRACK_FILE = "data/production_detailed.csv"

def run():

    st.header("📊 Production Tracking (Advanced)")

    if not os.path.exists("data"):
        os.makedirs("data")

    # ---------- STYLE LOAD (ONLY ORDER FILES) ----------
    files = os.listdir("data")

    styles = []
    for f in files:
        if f.startswith("order_") and f.endswith(".csv"):
            style_name = f.replace("order_", "").replace(".csv", "")
            styles.append(style_name)

    # REMOVE summary or unwanted files (extra safety)
    styles = [s for s in styles if not s.lower().startswith("summary")]

    if not styles:
        st.warning("⚠️ No styles found. Run Count Calculator first")
        return

    selected_style = st.selectbox("Select Style", styles)

    # ---------- LOAD ORDER FILE ----------
    order_path = f"data/order_{selected_style}.csv"

    if not os.path.exists(order_path):
        st.error("❌ Order file missing")
        return

    order_df = pd.read_csv(order_path)

    # ---------- SAFETY CHECK ----------
    required_cols = ["Color", "Size", "Quantity"]
    if not all(col in order_df.columns for col in required_cols):
        st.error(f"❌ Missing columns in order file. Required: {required_cols}")
        st.stop()

    # ---------- CLEAN ORDER DATA ----------
    order_df["Color"] = order_df["Color"].astype(str).str.strip().str.title()
    order_df["Size"] = order_df["Size"].astype(str).str.strip().str.upper()
    order_df["Quantity"] = pd.to_numeric(order_df["Quantity"], errors="coerce").fillna(0)

    st.subheader("🎯 Target Plan")
    st.dataframe(order_df, use_container_width=True)

    # ---------- TRACK FILE ----------
    if not os.path.exists(TRACK_FILE):
        df = pd.DataFrame(columns=["Style", "Date", "Process", "Color", "Size", "Qty"])
        df.to_csv(TRACK_FILE, index=False)

    df = pd.read_csv(TRACK_FILE)

    # ---------- CLEAN TRACK DATA ----------
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce").fillna(0)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["Process"] = df["Process"].astype(str).str.strip().str.title()
    df["Color"] = df["Color"].astype(str).str.strip().str.title()
    df["Size"] = df["Size"].astype(str).str.strip().str.upper()

    # ---------- FILTER BY STYLE ----------
    if "Style" not in df.columns:
        df["Style"] = ""

    df_style = df[df["Style"] == selected_style]

    # ---------- INPUT ----------
    st.subheader("➕ Enter Production")

    entry_date = pd.to_datetime(st.date_input("Date", value=date.today()))
    process = st.text_input("Process")

    selected_color = st.selectbox("Color", order_df["Color"].unique())
    selected_size = st.selectbox("Size", order_df["Size"].unique())

    qty = st.number_input("Qty", 0)

    if st.button("Save"):

        process_clean = process.strip().title()
        color_clean = selected_color.strip().title()
        size_clean = selected_size.strip().upper()

        new = pd.DataFrame([[
            selected_style, entry_date, process_clean, color_clean, size_clean, qty
        ]], columns=["Style", "Date", "Process", "Color", "Size", "Qty"])

        df = pd.concat([df, new], ignore_index=True)

        df.to_csv(TRACK_FILE, index=False)

        st.success("✅ Saved")
        st.rerun()

    # ---------- PROCESS VIEW ----------
    st.subheader("📈 Size-wise Progress")

    if not df_style.empty:

        process_list = df_style["Process"].dropna().unique().tolist()

        selected_process = st.selectbox("Select Process", process_list)

        filtered_df = df_style[df_style["Process"] == selected_process]

        produced_df = filtered_df.groupby(["Color", "Size"])["Qty"].sum().reset_index()

        merged = pd.merge(order_df, produced_df, on=["Color", "Size"], how="left")

        merged["Qty"] = merged["Qty"].fillna(0)
        merged["Pending"] = merged["Quantity"] - merged["Qty"]

        merged.rename(columns={
            "Quantity": "Target",
            "Qty": "Produced"
        }, inplace=True)

        st.dataframe(merged, use_container_width=True)

        # ---------- METRICS ----------
        col1, col2, col3 = st.columns(3)
        col1.metric("🎯 Target", int(merged["Target"].sum()))
        col2.metric("✅ Produced", int(merged["Produced"].sum()))
        col3.metric("⏳ Pending", int(merged["Pending"].sum()))

    else:
        st.info("No production data for this style")

    # ---------- SUMMARY ----------
    st.subheader("📊 Process Summary")

    if not df_style.empty:
        summary = df_style.groupby(["Process", "Color"])["Qty"].sum().reset_index()
        st.dataframe(summary, use_container_width=True)

    # ---------- LOG ----------
    st.subheader("📋 Production Log")

    if not df_style.empty:
        df_display = df_style.sort_values(by="Date", ascending=False)
        st.dataframe(df_display, use_container_width=True)

    # ---------- DELETE ----------
    st.subheader("🗑️ Delete Entry")

    if not df_style.empty:
        idx = st.number_input("Row No", 0, len(df_style)-1, 0)

        if st.button("Delete Row"):
            df = df.drop(df_style.index[idx]).reset_index(drop=True)
            df.to_csv(TRACK_FILE, index=False)
            st.success("Deleted")
            st.rerun()

    # ---------- CLEAR ----------
    st.subheader("⚠️ Danger Zone")

    if st.button("Clear This Style Data"):
        df = df[df["Style"] != selected_style]
        df.to_csv(TRACK_FILE, index=False)
        st.success("Cleared this style data")
        st.rerun()

    if st.button("Clear ALL Production Data"):
        df = pd.DataFrame(columns=["Style", "Date", "Process", "Color", "Size", "Qty"])
        df.to_csv(TRACK_FILE, index=False)
        st.success("All data cleared")
        st.rerun()
