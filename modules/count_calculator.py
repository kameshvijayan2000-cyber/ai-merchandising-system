import streamlit as st
import pandas as pd
import math
import os

# FILES
DETAIL_FILE = "data/order_details.csv"
STYLE_FILE = "data/order_styles.csv"

# -------- LOGIC FUNCTION --------
def calculate_order_distribution(base_per_ratio, color_ratios):

    result_rows = []
    summary_rows = []

    for color, sizes in color_ratios.items():

        color_total = 0
        units_per_pack = 0

        for size, ratio in sizes.items():

            qty = ratio * base_per_ratio
            color_total += qty
            units_per_pack += ratio

            result_rows.append({
                "Color": color,
                "Size": size,
                "Ratio": ratio,
                "Quantity": qty
            })

        summary_rows.append({
            "Color": color,
            "Total Quantity": color_total,
            "Units / Pack": units_per_pack
        })

    df_detail = pd.DataFrame(result_rows)
    df_summary = pd.DataFrame(summary_rows)

    return df_detail, df_summary


# -------- MAIN MODULE --------
def count_calculator_module():

    st.header("📦 Order Count Calculator (Advanced)")

    # ---------- FOLDER ----------
    if not os.path.exists("data"):
        os.makedirs("data")

    # ---------- STYLE LIST ----------
    styles = []
    if os.path.exists(STYLE_FILE):
        styles = pd.read_csv(STYLE_FILE)["Style"].dropna().unique().tolist()

    selected_style = st.selectbox("Select Style", ["New"] + styles)

    product_name = st.text_input("Style Name")

    # ---------- CARTON INPUT ----------
    st.subheader("Carton Planning")

    cartons = st.number_input("Number of Cartons", value=270)
    pcs_per_carton = st.number_input("Pieces per Carton", value=1)
    extra_percent = st.number_input("Extra % (Carton)", value=5.0)

    base_qty = cartons * pcs_per_carton
    extra_qty = math.ceil(base_qty * extra_percent / 100)
    final_carton_qty = math.ceil(cartons + (cartons * extra_percent / 100))

    st.info(f"Base Quantity: {base_qty}")
    st.info(f"Extra Quantity: {extra_qty}")
    st.success(f"Final Carton Quantity (Per Ratio Unit): {final_carton_qty}")

    # ---------- SIZE ----------
    size_input = st.text_input("Sizes", "XS,S,M,L,XL")
    sizes_list = [s.strip() for s in size_input.split(",") if s.strip()]

    # ---------- COLORS ----------
    num_colors = st.number_input("Number of Colors", 1, 10, 1)

    color_ratios = {}

    for i in range(int(num_colors)):

        st.subheader(f"Color {i+1}")

        color_name = st.text_input(f"Color Name {i+1}", key=f"color_{i}")

        size_ratios = {}

        for size in sizes_list:
            ratio = st.number_input(
                f"{size} Ratio",
                min_value=0,
                value=1,
                key=f"{size}_{i}"
            )
            size_ratios[size] = ratio

        if color_name:
            color_ratios[color_name] = size_ratios

    # ---------- CALCULATE ----------
    if st.button("🚀 Calculate Order Distribution"):

        if not product_name:
            st.warning("Enter Style Name")
            return

        df_detail, df_summary = calculate_order_distribution(
            final_carton_qty,
            color_ratios
        )

        # SAVE FILES
        detail_file = f"data/order_{product_name}.csv"
        summary_file = f"data/order_summary_{product_name}.csv"

        df_detail.to_csv(detail_file, index=False)
        df_summary.to_csv(summary_file, index=False)

        # SAVE STYLE NAME
        pd.DataFrame([[product_name]], columns=["Style"]).to_csv(
            STYLE_FILE,
            mode="a",
            header=not os.path.exists(STYLE_FILE),
            index=False
        )

        st.success("✅ Style Saved Successfully")

        # DISPLAY
        st.subheader("📊 Size-wise Breakdown")
        st.dataframe(df_detail, use_container_width=True)

        st.subheader("🎨 Color-wise Summary")
        st.dataframe(df_summary, use_container_width=True)

        st.metric("📦 Total Order Qty", int(df_detail["Quantity"].sum()))

    # ---------- LOAD OLD STYLE ----------
    if selected_style != "New":

        detail_file = f"data/order_{selected_style}.csv"
        summary_file = f"data/order_summary_{selected_style}.csv"

        if os.path.exists(detail_file) and os.path.exists(summary_file):

            df_detail = pd.read_csv(detail_file)
            df_summary = pd.read_csv(summary_file)

            st.subheader(f"📂 Loaded Style: {selected_style}")

            st.subheader("📊 Size-wise Breakdown")
            st.dataframe(df_detail, use_container_width=True)

            st.subheader("🎨 Color-wise Summary")
            st.dataframe(df_summary, use_container_width=True)

        else:
            st.warning("⚠️ Style data missing")

    # ---------- DELETE ----------
    if selected_style != "New":
        if st.button("🗑️ Delete This Style"):

            detail_file = f"data/order_{selected_style}.csv"
            summary_file = f"data/order_summary_{selected_style}.csv"

            if os.path.exists(detail_file):
                os.remove(detail_file)

            if os.path.exists(summary_file):
                os.remove(summary_file)

            if os.path.exists(STYLE_FILE):
                styles_df = pd.read_csv(STYLE_FILE)
                styles_df = styles_df[styles_df["Style"] != selected_style]
                styles_df.to_csv(STYLE_FILE, index=False)

            st.success("✅ Style Deleted")
            st.rerun()

    # ================= NEW FEATURE =================
    st.markdown("---")
    st.subheader("📦 All Styles Color-wise Summary")

    if styles:

        all_rows = []

        for style in styles:

            summary_file = f"data/order_summary_{style}.csv"

            if os.path.exists(summary_file):

                temp_df = pd.read_csv(summary_file)
                temp_df["Style"] = style

                all_rows.append(temp_df)

        if all_rows:

            final_df = pd.concat(all_rows, ignore_index=True)

            # ---------- STYLE WISE ----------
            for style in final_df["Style"].unique():

                st.markdown(f"### 🧵 Style: {style}")

                style_df = final_df[final_df["Style"] == style]

                st.dataframe(style_df, use_container_width=True)

            # ---------- GRAND TOTAL ----------
            st.markdown("### 📊 Grand Total")

            total_df = final_df.groupby("Color")["Total Quantity"].sum().reset_index()

            st.dataframe(total_df, use_container_width=True)

        else:
            st.info("No summary data available")

    else:
        st.info("No styles saved yet")
