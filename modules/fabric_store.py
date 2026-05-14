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
    st.subheader("➕ Add Roll")

    col1, col2 = st.columns(2)

    with col1:
        roll = st.text_input("Roll No")
        fabric = st.text_input("Fabric")

    with col2:
        color = st.text_input("Color")

        kg = st.number_input(
            "Kg",
            min_value=0.0,
            format="%.2f"
        )

    # ================= SAVE =================
    if st.button("💾 Add Roll"):

        if not roll or not fabric or not color:

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

            save_json(FILE, data)

            st.success("✅ Roll Added Successfully")

            st.rerun()

    # ================= DISPLAY =================
    st.markdown("---")

    st.subheader("📦 Current Fabric Stock")

    df = pd.DataFrame(data["rolls"])

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

        # ================= SUMMARY =================
        st.subheader("📊 Fabric Summary")

        summary_df = df.groupby(
            ["Fabric", "Color"]
        )["Kg"].sum().reset_index()

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # ================= TOTAL =================
        st.metric(
            "🧵 Total Kg",
            round(df["Kg"].sum(), 2)
        )

        # ================= DELETE SINGLE ROW =================
        st.markdown("---")

        st.subheader("🗑️ Delete Roll")

        delete_index = st.number_input(
            "Enter Row Number",
            min_value=0,
            max_value=len(df) - 1,
            step=1
        )

        if st.button("❌ Delete Selected Roll"):

            data["rolls"].pop(delete_index)

            save_json(FILE, data)

            st.success("Roll Deleted Successfully")

            st.rerun()

    else:

        st.info("No Fabric Rolls Added")

    # ================= CLEAR =================
    st.markdown("---")

    st.warning(
        "⚠️ Clear button will permanently remove all fabric stock data"
    )

    if st.button("🗑️ Clear Fabric Store"):

        data["rolls"] = []

        save_json(FILE, data)

        st.success("All Fabric Store Data Cleared")

        st.rerun()