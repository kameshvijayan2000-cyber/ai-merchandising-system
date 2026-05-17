import streamlit as st
import pandas as pd
from datetime import date
from modules.utils import load_json, save_json

FILE = "data/production_tracking.json"


def run():

    st.header("🏭 Production Tracker")

    data = load_json(FILE)

    # ================= INITIALIZE =================
    if "entries" not in data:
        data["entries"] = []

    # ================= INPUT SECTION =================
    st.subheader("➕ Add Production Entry")

    col1, col2 = st.columns(2)

    with col1:

        process = st.selectbox(

            "Process",

            [
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
        )

        custom_process = st.text_input(
            "Or Add Custom Process"
        )

        if custom_process:
            process = custom_process

        entry_type = st.selectbox(
            "Type",
            ["Input", "Output"]
        )

        entry_date = st.date_input(
            "Date",
            value=date.today()
        )

    with col2:

        qty = st.number_input(
            "Qty",
            min_value=0.0,
            format="%.2f"
        )

        party = st.text_input(
            "Party / Unit"
        )

        rate = st.number_input(
            "Rate",
            min_value=0.0,
            format="%.2f"
        )

        description = st.text_input(
            "Description"
        )

    # ================= UNIT =================
    if process in [

        "Cutting",
        "Stitching",
        "Checking",
        "Ironing",
        "Packing"

    ]:

        unit = "PCS"

    else:

        unit = "KG"

    total = qty * rate

    # ================= LIVE INFO =================
    col3, col4 = st.columns(2)

    with col3:

        st.info(
            f"📦 Unit : {unit}"
        )

    with col4:

        st.success(
            f"💰 Total Cost : ₹ {round(total,2)}"
        )

    # ================= SAVE =================
    if st.button("💾 Save Entry"):

        data["entries"].append({

            "Date": str(entry_date),

            "Process": process,

            "Type": entry_type,

            "Qty": qty,

            "Unit": unit,

            "Party": party,

            "Description": description,

            "Rate": rate,

            "Total": total
        })

        save_json(FILE, data)

        st.success(
            "✅ Entry Saved Successfully"
        )

        st.rerun()

    # ================= DISPLAY =================
    st.markdown("---")

    df = pd.DataFrame(
        data["entries"]
    )

    if not df.empty:

        # ================= TABLE =================
        st.subheader(
            "📊 Production Entries"
        )

        display_df = df.copy()

        display_df.index = (
            display_df.index + 1
        )

        st.dataframe(
            display_df,
            use_container_width=True
        )

        # ================= TOP METRICS =================
        st.markdown("---")

        total_entries = len(df)

        total_qty = round(
            df["Qty"].sum(),
            2
        )

        total_cost = round(
            df["Total"].sum(),
            2
        )

        total_process = df[
            "Process"
        ].nunique()

        col5, col6, col7, col8 = st.columns(4)

        with col5:

            st.metric(
                "📋 Entries",
                total_entries
            )

        with col6:

            st.metric(
                "📦 Total Qty",
                total_qty
            )

        with col7:

            st.metric(
                "🏭 Processes",
                total_process
            )

        with col8:

            st.metric(
                "💰 Total Cost",
                f"₹ {total_cost}"
            )

        # ================= STAGE SUMMARY =================
        st.markdown("---")

        st.subheader(
            "📈 Stage Summary"
        )

        summary = []

        for p in df["Process"].unique():

            process_df = df[
                df["Process"] == p
            ]

            input_qty = process_df[
                process_df["Type"] == "Input"
            ]["Qty"].sum()

            output_qty = process_df[
                process_df["Type"] == "Output"
            ]["Qty"].sum()

            balance = (
                input_qty - output_qty
            )

            summary.append({

                "Process": p,

                "Input":
                round(input_qty, 2),

                "Output":
                round(output_qty, 2),

                "Balance":
                round(balance, 2)
            })

        summary_df = pd.DataFrame(
            summary
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # ================= COST SUMMARY =================
        st.markdown("---")

        st.subheader(
            "💰 Cost Summary"
        )

        cost_summary = df.groupby(
            "Process"
        )["Total"].sum().reset_index()

        cost_summary.columns = [

            "Process",
            "Total Cost"

        ]

        cost_summary["Total Cost"] = (
            cost_summary["Total Cost"]
            .round(2)
        )

        st.dataframe(
            cost_summary,
            use_container_width=True
        )

        # ================= PARTY SUMMARY =================
        st.markdown("---")

        st.subheader(
            "🏢 Party Summary"
        )

        party_summary = df.groupby(
            "Party"
        )["Total"].sum().reset_index()

        party_summary.columns = [

            "Party",
            "Total Cost"

        ]

        party_summary["Total Cost"] = (
            party_summary["Total Cost"]
            .round(2)
        )

        st.dataframe(
            party_summary,
            use_container_width=True
        )

    else:

        st.info(
            "No Production Entries Added"
        )

    # ================= DELETE ROW =================
    st.markdown("---")

    st.subheader(
        "🗑️ Delete Entry"
    )

    if not df.empty:

        delete_index = st.number_input(

            "Select Row Number",

            min_value=1,

            max_value=len(df),

            step=1
        )

        if st.button(
            "❌ Delete Selected Entry"
        ):

            data["entries"].pop(
                delete_index - 1
            )

            save_json(
                FILE,
                data
            )

            st.success(
                "Entry Deleted Successfully"
            )

            st.rerun()

    # ================= CLEAR =================
    st.markdown("---")

    st.warning(
        "⚠️ This will permanently delete all production tracking data"
    )

    if st.button(
        "🗑️ Clear Production Data"
    ):

        data["entries"] = []

        save_json(
            FILE,
            data
        )

        st.success(
            "All Production Data Cleared"
        )

        st.rerun()