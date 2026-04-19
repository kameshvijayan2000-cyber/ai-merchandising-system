import streamlit as st
import pandas as pd
import math

# -------- LOGIC FUNCTION --------
def calculate_order_distribution(base_per_ratio, color_ratios):

    result_rows = []
    summary_rows = []

    for color, sizes in color_ratios.items():

        color_total = 0

        for size, ratio in sizes.items():

            qty = ratio * base_per_ratio   # ✅ YOUR REQUIRED LOGIC

            color_total += qty

            result_rows.append({
                "Color": color,
                "Size": size,
                "Ratio": ratio,
                "Quantity": qty
            })

        summary_rows.append({
            "Color": color,
            "Total Quantity": color_total
        })

    df_detail = pd.DataFrame(result_rows)
    df_summary = pd.DataFrame(summary_rows)

    return df_detail, df_summary


# -------- STREAMLIT UI --------
def count_calculator_module():

    st.header("📦 Order Count Calculator (Advanced)")

    product_name = st.text_input("Product Name")

    # -------- CARTON INPUT --------
    st.subheader("Carton Planning")

    cartons = st.number_input("Number of Cartons", value=270)
    pcs_per_carton = st.number_input("Pieces per Carton", value=1)
    extra_percent = st.number_input("Extra % (Carton)", value=5.0)

    base_qty = cartons * pcs_per_carton

    # ✅ ALWAYS ROUND UP
    extra_qty = math.ceil(base_qty * extra_percent / 100)
    final_carton_qty = math.ceil(cartons + (cartons * extra_percent / 100))

    st.info(f"Base Quantity: {base_qty}")
    st.info(f"Extra Quantity: {extra_qty}")
    st.success(f"Final Carton Quantity (Per Ratio Unit): {final_carton_qty}")

    # -------- SIZE INPUT --------
    size_input = st.text_input("Sizes (comma separated)", "XS,S,M,L,XL")
    sizes_list = [s.strip() for s in size_input.split(",") if s.strip()]

    # -------- COLOR INPUT --------
    num_colors = st.number_input("Number of Colors", min_value=1, max_value=10, value=1)

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

    # -------- CALCULATE --------
    if st.button("🚀 Calculate Order Distribution"):

        if not color_ratios:
            st.warning("Please enter at least one color name")
            return

        df_detail, df_summary = calculate_order_distribution(
            final_carton_qty,
            color_ratios
        )

        # ✅ SAVE FOR PLANNING MODULE
        st.session_state["order_detail"] = df_detail
        st.session_state["order_summary"] = df_summary

        st.success("✅ Data saved for Production Tracking")

        # -------- DISPLAY --------
        st.subheader("Size-wise Quantity")
        st.dataframe(df_detail, use_container_width=True)

        st.subheader("Color-wise Total")
        st.dataframe(df_summary, use_container_width=True)

        # -------- DOWNLOAD --------
        file_name = f"{product_name}_Order_Count.xlsx"

        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df_detail.to_excel(writer, sheet_name="Size Wise", index=False)
            df_summary.to_excel(writer, sheet_name="Color Summary", index=False)

        with open(file_name, "rb") as f:
            st.download_button("Download Excel", f, file_name=file_name)
