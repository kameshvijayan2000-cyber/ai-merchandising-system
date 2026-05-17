import streamlit as st
import pandas as pd
from modules.utils import load_json, save_json

FILE = "data/fabric_store.json"


def run():

    st.header("🧵 Fabric Store")

    # ================= LOAD DATA =================
    data = load_json(FILE)

    if "rolls" not in data:
        data["rolls"] = []

    # ================= ADD ROLL =================
    st.subheader("➕ Add Fabric Roll")

    col1, col2 = st.columns(2)

    with col1:

        roll = st.text_input(
            "Roll No"
        )

        fabric = st.text_input(
            "Fabric Type"
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
    if st.button("💾 Add Roll"):

        if (
            not roll or
            not fabric or
            not color
        ):

            st.warning(
                "Please fill all fields"
            )

        else:

            data["rolls"].append({

                "Roll No": roll,

                "Fabric": fabric,

                "Color": color,

                "Kg": kg
            })

            save_json(
                FILE,
                data
            )

            st.success(
                "✅ Roll Added Successfully"
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

        # ================= STOCK TABLE =================
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

        total_rolls = len(df)

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
            "📊 Fabric Summary"
        )

        fabric_summary = df.groupby(
            "Fabric"
        )["Kg"].sum().reset_index()

        fabric_summary["Kg"] = (
            fabric_summary["Kg"]
            .round(2)
        )

        st.dataframe(
            fabric_summary,
            use_container_width=True
        )

        # ================= COLOR SUMMARY =================
        st.markdown("---")

        st.subheader(
            "🎨 Color Summary"
        )

        color_summary = df.groupby(
            "Color"
        )["Kg"].sum().reset_index()

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
        )["Kg"].sum().reset_index()

        summary_df["Kg"] = (
            summary_df["Kg"]
            .round(2)
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # ================= DELETE ROLL =================
        st.markdown("---")

        st.subheader(
            "🗑️ Delete Roll"
        )

        delete_index = st.number_input(
            "Select Row Number",
            min_value=1,
            max_value=len(df),
            step=1
        )

        if st.button(
            "❌ Delete Selected Roll"
        ):

            data["rolls"].pop(
                delete_index - 1
            )

            save_json(
                FILE,
                data
            )

            st.success(
                "Roll Deleted Successfully"
            )

            st.rerun()

    else:

        st.info(
            "No Fabric Rolls Added"
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