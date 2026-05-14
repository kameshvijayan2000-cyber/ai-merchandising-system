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
    st.subheader("➕ Add Entry")

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

    qty = st.number_input(
        "Qty",
        min_value=0.0
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

    party = st.text_input("Party")

    description = st.text_input(
        "Description"
    )

    rate = st.number_input(
        "Rate",
        min_value=0.0
    )

    total = qty * rate

    st.info(f"Unit : {unit}")

    st.success(
        f"Total Cost : ₹ {round(total,2)}"
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

        st.success("✅ Entry Saved")

        st.rerun()

    # ================= DISPLAY =================
    st.markdown("---")

    df = pd.DataFrame(data["entries"])

    if not df.empty:

        st.subheader("📊 All Entries")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ================= STAGE SUMMARY =================
        st.subheader("📈 Stage Summary")

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
        st.subheader("💰 Cost Summary")

        cost_summary = df.groupby(
            "Process"
        )["Total"].sum().reset_index()

        cost_summary.columns = [
            "Process",
            "Total Cost"
        ]

        st.dataframe(
            cost_summary,
            use_container_width=True
        )

        st.metric(
            "Total Cost",
            f"₹ {round(df['Total'].sum(),2)}"
        )

    # ================= DELETE ROW =================
    st.markdown("---")

    st.subheader("🗑️ Delete Entry")

    if not df.empty:

        selected_index = st.number_input(

            "Select Row Number",

            min_value=0,

            max_value=len(df) - 1,

            step=1
        )

        if st.button("Delete Row"):

            data["entries"].pop(
                selected_index
            )

            save_json(FILE, data)

            st.success(
                "✅ Row Deleted"
            )

            st.rerun()

    # ================= CLEAR =================
    st.markdown("---")

    if st.button(
        "🗑️ Clear Production Data"
    ):

        data["entries"] = []

        save_json(FILE, data)

        st.warning(
            "All production data cleared"
        )

        st.rerun()