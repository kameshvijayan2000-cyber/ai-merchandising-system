import streamlit as st
import pandas as pd
import os

FILE = "data/fabric_stock.csv"

def run():
    st.header("🧵 Fabric Store")

    # Create folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Create file if not exists
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=["Roll No", "Fabric Type", "Color", "Kg"])
        df.to_csv(FILE, index=False)

    # Read safely
    df = pd.read_csv(FILE, dtype=str)

    if "Kg" in df.columns:
        df["Kg"] = pd.to_numeric(df["Kg"], errors="coerce").fillna(0)

    # Add new roll
    st.subheader("➕ Add Fabric Roll")

    roll = st.text_input("Roll No")
    fabric = st.text_input("Fabric Type")
    color = st.text_input("Color")
    kg = st.number_input("Weight (kg)", min_value=0.0)

    if st.button("Add Roll"):
        if not roll or not fabric or not color:
            st.warning("Please fill all fields")
        else:
            new = pd.DataFrame(
                [[str(roll), str(fabric), str(color), float(kg)]],
                columns=["Roll No", "Fabric Type", "Color", "Kg"]
            )

            df = pd.concat([df, new], ignore_index=True)
            df.to_csv(FILE, index=False)

            st.success("✅ Added Successfully")
            st.rerun()

    # Display
    st.subheader("📦 Current Stock")

    st.dataframe(df.astype({
        "Roll No": str,
        "Fabric Type": str,
        "Color": str,
        "Kg": float
    }), use_container_width=True)

    st.metric("Total Fabric", f"{round(df['Kg'].sum(),2)} kg")

    # ✅ CLEAR DATA BUTTON (INSIDE FUNCTION)
    if st.button("🗑️ Clear All Fabric Data"):
        df = pd.DataFrame(columns=["Roll No", "Fabric Type", "Color", "Kg"])
        df.to_csv(FILE, index=False)
        st.warning("All fabric data cleared!")
        st.rerun()
