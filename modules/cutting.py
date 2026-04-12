<<<<<<< HEAD
import streamlit as st
import pandas as pd
import os

FILE = "data/cutting_data.csv"

def run():   # ✅ IMPORTANT NAME

    st.header("✂️ Cutting Entry")

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Lay Length", "Plies", "Pieces", "Consumption", "Wastage %"
        ])
        df.to_csv(FILE, index=False)

    df = pd.read_csv(FILE)

    lay = st.number_input("Lay Length (m)")
    plies = st.number_input("Plies", value=50)
    pieces = st.number_input("Pieces Cut")
    cons = st.number_input("Consumption per piece")

    if st.button("Calculate & Save"):

        total = lay * plies
        actual = pieces * cons
        wastage = ((total - actual) / total) * 100 if total != 0 else 0

        new = pd.DataFrame(
            [[lay, plies, pieces, cons, round(wastage, 2)]],
            columns=df.columns
        )

        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)

        st.success(f"✅ Wastage: {round(wastage, 2)}%")

    st.subheader("📋 Cutting History")
    st.dataframe(df)
=======
import streamlit as st
import pandas as pd
import os

FILE = "data/cutting_data.csv"

def run():   # ✅ IMPORTANT NAME

    st.header("✂️ Cutting Entry")

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "Lay Length", "Plies", "Pieces", "Consumption", "Wastage %"
        ])
        df.to_csv(FILE, index=False)

    df = pd.read_csv(FILE)

    lay = st.number_input("Lay Length (m)")
    plies = st.number_input("Plies", value=50)
    pieces = st.number_input("Pieces Cut")
    cons = st.number_input("Consumption per piece")

    if st.button("Calculate & Save"):

        total = lay * plies
        actual = pieces * cons
        wastage = ((total - actual) / total) * 100 if total != 0 else 0

        new = pd.DataFrame(
            [[lay, plies, pieces, cons, round(wastage, 2)]],
            columns=df.columns
        )

        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(FILE, index=False)

        st.success(f"✅ Wastage: {round(wastage, 2)}%")

    st.subheader("📋 Cutting History")
    st.dataframe(df)
>>>>>>> 542cdebd01ea9baf46f7d3618875dfb4a486bc55
