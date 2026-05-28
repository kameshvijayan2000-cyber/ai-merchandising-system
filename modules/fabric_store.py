import streamlit as st
import pandas as pd
from datetime import date
from modules.utils import load_json, save_json

FILE = "data/fabric_store.json"


def run():

    st.header("🧵 Fabric Store")

    # ================= LOAD DATA =================
    data = load_json(FILE)

    if "rolls" not in data:
        data["rolls"] = []

    # ================= FIX OLD DATA =================
    for item in data["rolls"]:

        if "Rolls" not in item:
            item["Rolls"] = 1

        if "Date" not in item:
            item["Date"] = str(date.today())

        if "Company" not in item:
            item["Company"] = "Unknown"

    # ================= ADD FABRIC =================
    st.subheader("➕ Add Fabric Stock")

    col1, col2 = st.columns(2)

    with col1:

        entry_date = st.date_input(
            "Date",
            value=date.today()
        )

        fabric = st.text_input(
            "Fabric Type"
        )

        company = st.text_input(
            "Company Name"
        )

        no_of_rolls = st.number_input(
            "No Of Rolls",
            min_value=1,
            value=1
        )

    with col2:

        color = st.text_input(
            "Color"
        )

        kg = st.number_input(
            "Weight (Kg)",
            min_value=0.0,
            format="%.2f"
        )

    # ================= SAVE =================
    if st.button("💾 Add Fabric"):

        if (
            not fabric or
            not color or
            not company
        ):

            st.warning(
                "Please fill all fields"
            )

        else:

            data["rolls"].append({

                "Date": str(entry_date),

                "Company": company,

                "Fabric": fabric,

                "Color": color,

                "Rolls": int(no_of_rolls),

                "Kg": float(kg)
            })

            save_json(
                FILE,
                data
            )

            st.success(
                "✅ Fabric Added Successfully"
            )

            st.rerun()

    # ================= DISPLAY =================
    st.markdown("---")

    st.subheader(
        "📦 Current Fabric Stock"
    )

    df = pd.DataFrame(
        data["rolls"]
    )

    if not df.empty:

        # ================= FIX COLUMNS =================
        if "Rolls" not in df.columns:
            df["Rolls"] = 1

        if "Date" not in df.columns:
            df["Date"] = str(date.today())

        if "Company" not in df.columns:
            df["Company"] = "Unknown"

        # ================= DISPLAY TABLE =================
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

        total_rolls = int(
            df["Rolls"].sum()
        )

        total_kg = round(
            df["Kg"].sum(),
            2
        )

        total_colors = df[
            "Color"
        ].nunique()

        total_fabrics = df[
            "Fabric"
        ].nunique()

        col3, col4, col5, col6 = st.columns(4)

        with col3:

            st.metric(
                "🎯 Total Rolls",
                total_rolls
            )

        with col4:

            st.metric(
                "🧵 Total Kg",
                total_kg
            )

        with col5:

            st.metric(
                "🎨 Colors",
                total_colors
            )

        with col6:

            st.metric(
                "📦 Fabric Types",
                total_fabrics
            )

        # ================= FABRIC SUMMARY =================
        st.markdown("---")

        st.subheader(
            "📊 Fabric Type Summary"
        )

        fabric_summary = df.groupby(
            "Fabric"
        ).agg({

            "Rolls": "sum",

            "Kg": "sum"

        }).reset_index()

        fabric_summary["Kg"] = (
            fabric_summary["Kg"]
            .round(2)
        )

        st.dataframe(
            fabric_summary,
            use_container_width=True
        )

        # ================= COMPANY SUMMARY =================
        st.markdown("---")

        st.subheader(
            "🏢 Company Summary"
        )

        company_summary = df.groupby(
            "Company"
        ).agg({

            "Rolls": "sum",

            "Kg": "sum"

        }).reset_index()

        company_summary["Kg"] = (
            company_summary["Kg"]
            .round(2)
        )

        st.dataframe(
            company_summary,
            use_container_width=True
        )

        # ================= COLOR SUMMARY =================
        st.markdown("---")

        st.subheader(
            "🎨 Color Summary"
        )

        color_summary = df.groupby(
            "Color"
        ).agg({

            "Rolls": "sum",

            "Kg": "sum"

        }).reset_index()

        color_summary["Kg"] = (
            color_summary["Kg"]
            .round(2)
        )

        st.dataframe(
            color_summary,
            use_container_width=True
        )

        # ================= FABRIC + COLOR SUMMARY =================
        st.markdown("---")

        st.subheader(
            "📦 Fabric + Color Summary"
        )

        summary_df = df.groupby(
            ["Fabric", "Color"]
        ).agg({

            "Rolls": "sum",

            "Kg": "sum"

        }).reset_index()

        summary_df["Kg"] = (
            summary_df["Kg"]
            .round(2)
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # ================= DATE SUMMARY =================
        st.markdown("---")

        st.subheader(
            "📅 Date Wise Summary"
        )

        date_summary = df.groupby(
            "Date"
        ).agg({

            "Rolls": "sum",

            "Kg": "sum"

        }).reset_index()

        date_summary["Kg"] = (
            date_summary["Kg"]
            .round(2)
        )

        st.dataframe(
            date_summary,
            use_container_width=True
        )

        # ================= DELETE =================
        st.markdown("---")

        st.subheader(
            "🗑️ Delete Entry"
        )

        delete_index = st.number_input(
            "Select Row Number",
            min_value=1,
            max_value=len(df),
            step=1
        )

        if st.button(
            "❌ Delete Selected Entry"
        ):

            data["rolls"].pop(
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

    else:

        st.info(
            "No Fabric Stock Added"
        )

    # ================= CLEAR STORE =================
    st.markdown("---")

    st.warning(
        "⚠️ This will permanently delete all fabric store data"
    )

    if st.button(
        "🗑️ Clear Fabric Store"
    ):

        data["rolls"] = []

        save_json(
            FILE,
            data
        )

        st.success(
            "All Fabric Store Data Cleared"
        )

        st.rerun()