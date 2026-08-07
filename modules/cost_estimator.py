import streamlit as st
import pandas as pd
from modules.utils import load_json, save_json

FILE = "data/cost_estimator.json"

def run():

    st.header("💰 Cost Estimator")
    # ================= LOAD DATA =================

    data = load_json(FILE)

    if not isinstance(data, dict):
        data = {}

    st.markdown("---")

    # =========================================================
    # BASIC DETAILS
    # =========================================================

    st.subheader("📋 Style Details")

    style_name = st.text_input(
        "Style Name"
    )

    order_qty = st.number_input(
        "Order Quantity",
        min_value=1,
        value=1000
    )

    # =========================================================
    # FABRIC EXCESS
    # =========================================================

    st.markdown("---")

    st.subheader("🧵 Fabric Process Qty")

    fabric_excess_percent = st.number_input(
        "Fabric Process Excess %",
        value=7.0
    )

    final_fabric_qty = order_qty * (
        1 +
        fabric_excess_percent / 100
    )

    st.success(
        f"Final Fabric Qty : {round(final_fabric_qty, 0)} PCS"
    )

    # =========================================================
    # SIZE INPUT
    # =========================================================

    st.markdown("---")

    st.subheader("📏 Sizes")

    size_input = st.text_input(
        "Enter Sizes",
        value="XS,S,M,L,XL"
    )

    sizes = [

        x.strip()

        for x in size_input.split(",")

        if x.strip()
    ]

    # =========================================================
    # BODY
    # =========================================================

    st.markdown("---")

    st.subheader("👕 Body")

    include_body = st.checkbox(
        "Include Body",
        value=True
    )

    body_gsm = 0

    if include_body:

        body_gsm = st.number_input(
            "Body GSM",
            value=220.0
        )

    # =========================================================
    # SLEEVE
    # =========================================================

    st.markdown("---")

    st.subheader("🦾 Sleeve")

    include_sleeve = st.checkbox(
        "Include Sleeve",
        value=True
    )

    sleeve_gsm = 0

    if include_sleeve:

        sleeve_gsm = st.number_input(
            "Sleeve GSM",
            value=220.0
        )

    # =========================================================
    # BOTTOM RIB
    # =========================================================

    st.markdown("---")

    st.subheader("📏 Bottom Rib")

    include_bottom_rib = st.checkbox(
        "Include Bottom Rib",
        value=False
    )

    bottom_rib_gsm = 0

    if include_bottom_rib:

        bottom_rib_gsm = st.number_input(
            "Bottom Rib GSM",
            value=320.0
        )

    # =========================================================
    # CUFF
    # =========================================================

    st.markdown("---")

    st.subheader("✋ Hand Cuff")

    include_cuff = st.checkbox(
        "Include Hand Cuff",
        value=False
    )

    cuff_gsm = 0

    if include_cuff:

        cuff_gsm = st.number_input(
            "Cuff GSM",
            value=320.0
        )

    # =========================================================
    # NECK
    # =========================================================

    st.markdown("---")

    st.subheader("🧣 Neck Rib")

    include_neck = st.checkbox(
        "Include Neck Rib",
        value=False
    )

    neck_gsm = 0

    if include_neck:

        neck_gsm = st.number_input(
            "Neck Rib GSM",
            value=320.0
        )

    # =========================================================
    # HOODIE
    # =========================================================

    st.markdown("---")

    st.subheader("🧥 Hoodie")

    include_hoodie = st.checkbox(
        "Include Hoodie",
        value=False
    )

    hoodie_gsm = 0

    if include_hoodie:

        hoodie_gsm = st.number_input(
            "Hoodie GSM",
            value=220.0
        )

    # =========================================================
    # MEASUREMENTS
    # =========================================================

    st.markdown("---")

    st.subheader("📐 Measurement Inputs")

    piece_rows = []

    # =========================================================
    # SIZE LOOP
    # =========================================================

    for size in sizes:

        st.markdown("---")

        st.write(f"## Size : {size}")

        total_weight = 0

        # =====================================================
        # BODY
        # =====================================================

        if include_body:

            col1, col2 = st.columns(2)

            with col1:

                body_length = st.number_input(
                    f"{size} Body Length",
                    value=70.0,
                    key=f"body_length_{size}"
                )

            with col2:

                body_width = st.number_input(
                    f"{size} Body Width",
                    value=55.0,
                    key=f"body_width_{size}"
                )

            body_area = (
                body_length *
                body_width *
                2
            )

            body_weight = (
                body_area *
                body_gsm
            ) / 10000

            total_weight += body_weight

        # =====================================================
        # SLEEVE
        # =====================================================

        if include_sleeve:

            col3, col4 = st.columns(2)

            with col3:

                sleeve_length = st.number_input(
                    f"{size} Sleeve Length",
                    value=24.0,
                    key=f"sleeve_length_{size}"
                )

            with col4:

                sleeve_width = st.number_input(
                    f"{size} Sleeve Width",
                    value=22.0,
                    key=f"sleeve_width_{size}"
                )

            sleeve_area = (
                sleeve_length *
                sleeve_width *
                4
            )

            sleeve_weight = (
                sleeve_area *
                sleeve_gsm
            ) / 10000

            total_weight += sleeve_weight

        # =====================================================
        # BOTTOM RIB
        # =====================================================

        if include_bottom_rib:

            col5, col6 = st.columns(2)

            with col5:

                bottom_length = st.number_input(
                    f"{size} Bottom Rib Length",
                    value=45.0,
                    key=f"bottom_length_{size}"
                )

            with col6:

                bottom_width = st.number_input(
                    f"{size} Bottom Rib Width",
                    value=8.0,
                    key=f"bottom_width_{size}"
                )

            bottom_area = (
                bottom_length *
                bottom_width *
                2
            )

            bottom_weight = (
                bottom_area *
                bottom_rib_gsm
            ) / 10000

            total_weight += bottom_weight

        # =====================================================
        # CUFF
        # =====================================================

        if include_cuff:

            col7, col8 = st.columns(2)

            with col7:

                cuff_length = st.number_input(
                    f"{size} Cuff Length",
                    value=10.0,
                    key=f"cuff_length_{size}"
                )

            with col8:

                cuff_width = st.number_input(
                    f"{size} Cuff Width",
                    value=8.0,
                    key=f"cuff_width_{size}"
                )

            cuff_area = (
                cuff_length *
                cuff_width *
                4
            )

            cuff_weight = (
                cuff_area *
                cuff_gsm
            ) / 10000

            total_weight += cuff_weight

        # =====================================================
        # NECK
        # =====================================================

        if include_neck:

            col9, col10 = st.columns(2)

            with col9:

                neck_length = st.number_input(
                    f"{size} Neck Length",
                    value=20.0,
                    key=f"neck_length_{size}"
                )

            with col10:

                neck_width = st.number_input(
                    f"{size} Neck Width",
                    value=5.0,
                    key=f"neck_width_{size}"
                )

            neck_area = (
                neck_length *
                neck_width *
                2
            )

            neck_weight = (
                neck_area *
                neck_gsm
            ) / 10000

            total_weight += neck_weight

        # =====================================================
        # HOODIE
        # =====================================================

        if include_hoodie:

            col11, col12 = st.columns(2)

            with col11:

                hoodie_length = st.number_input(
                    f"{size} Hoodie Length",
                    value=35.0,
                    key=f"hoodie_length_{size}"
                )

            with col12:

                hoodie_width = st.number_input(
                    f"{size} Hoodie Width",
                    value=30.0,
                    key=f"hoodie_width_{size}"
                )

            hoodie_area = (
                hoodie_length *
                hoodie_width *
                2
            )

            hoodie_weight = (
                hoodie_area *
                hoodie_gsm
            ) / 10000

            total_weight += hoodie_weight

        # =====================================================
        # SAVE ROW
        # =====================================================

        piece_rows.append({

            "Size":
            size,

            "Piece Weight (g)":
            round(total_weight, 3)
        })

    # =========================================================
    # DISPLAY PIECE WEIGHT
    # =========================================================

    st.markdown("---")

    st.subheader("📊 Piece Weight Summary")

    piece_df = pd.DataFrame(
        piece_rows
    )

    st.dataframe(
        piece_df,
        use_container_width=True
    )

    avg_piece_weight = piece_df[
        "Piece Weight (g)"
    ].mean()

    st.success(
        f"Average Piece Weight : {avg_piece_weight:.2f} g"
    )

    # =========================================================
    # FABRIC CALCULATION
    # =========================================================

    st.markdown("---")

    st.subheader("🧵 Fabric Costing")

    yarn_rate = st.number_input(
        "Yarn Rate / Kg",
        value=280.0
    )

    dyeing_rate = st.number_input(
        "Dyeing Rate / Kg",
        value=80.0
    )

    compacting_rate = st.number_input(
        "Compacting Rate / Kg",
        value=25.0
    )

    washing_rate = st.number_input(
        "Washing Rate / Kg",
        value=20.0
    )

    # =========================================================
    # EXTRA FABRIC PROCESS
    # =========================================================

    st.markdown("---")

    st.subheader("➕ Additional Fabric Processes")

    process_count = st.number_input(
        "No of Additional Processes",
        min_value=0,
        value=0
    )

    extra_process_total = 0

    for i in range(process_count):

        col13, col14 = st.columns(2)

        with col13:

            process_name = st.text_input(
                f"Process Name {i+1}",
                key=f"process_name_{i}"
            )

        with col14:

            process_rate = st.number_input(
                f"{process_name} Rate",
                value=0.0,
                key=f"process_rate_{i}"
            )

        extra_process_total += process_rate

    # =========================================================
    # FABRIC LOSS
    # =========================================================

    fabric_loss_percent = st.number_input(
    "Fabric Loss %",
    value=5.0
    )

    # Fabric consumption before loss
    base_fabric_kg = (
        avg_piece_weight *
        final_fabric_qty
    ) / 1000

    # Add fabric loss to consumption
    total_fabric_kg = (
        base_fabric_kg *
        (
            1 +
            fabric_loss_percent / 100
        )
    )

    fabric_rate = (

        yarn_rate +

        dyeing_rate +

        compacting_rate +

        washing_rate +

        extra_process_total
    )

    # Cost calculated on increased consumption
    final_fabric_amount = (
        total_fabric_kg *
        fabric_rate
    )

    # =========================================================
    # FABRIC SUMMARY
    # =========================================================

    st.markdown("---")

    st.subheader("🧵 Fabric Summary")

    fabric_summary = pd.DataFrame([{

        "Final Fabric Qty":
        round(final_fabric_qty, 0),

        "Avg Piece Weight (g)":
        round(avg_piece_weight, 2),

        "Total Fabric (Kg)":
        round(total_fabric_kg, 2),

        "Fabric Rate / Kg":
        round(fabric_rate, 2),

        "Fabric Amount":
        round(final_fabric_amount, 2)

    }])

    st.dataframe(
        fabric_summary,
        use_container_width=True
    )

    # =========================================================
    # TRIMS
    # =========================================================

    st.markdown("---")

    st.subheader("🎀 Trims & Accessories")

    trims_excess_percent = st.number_input(
        "Trims Excess %",
        value=5.0
    )

    trims_qty = order_qty * (
        1 +
        trims_excess_percent / 100
    )

    trim_count = st.number_input(
        "Number of Trims",
        min_value=1,
        value=1
    )

    trim_rows = []

    trims_total = 0

    for i in range(trim_count):

        col15, col16 = st.columns(2)

        with col15:

            trim_name = st.text_input(
                f"Trim Name {i+1}",
                key=f"trim_name_{i}"
            )

        with col16:

            trim_rate = st.number_input(
                f"{trim_name} Rate",
                value=0.0,
                key=f"trim_rate_{i}"
            )

        trim_amount = (
            trims_qty *
            trim_rate
        )

        trims_total += trim_amount

        trim_rows.append({

            "Trim":
            trim_name,

            "Rate":
            trim_rate,

            "Amount":
            round(trim_amount, 2)
        })

    trim_df = pd.DataFrame(
        trim_rows
    )

    st.dataframe(
        trim_df,
        use_container_width=True
    )

    st.success(
        f"Total Trims Cost : ₹ {round(trims_total, 2)}"
    )

    # =========================================================
    # OTHER COSTS
    # =========================================================

    st.markdown("---")

    st.subheader("🏭 Other Costs")

    cmt_value = st.number_input(
        "CMT Value",
        value=50.0
    )

    fob_value = st.number_input(
        "FOB Charges",
        value=20.0
    )

    # =========================================================
    # FINAL CALCULATION
    # =========================================================

    st.markdown("---")

    st.subheader("📈 Final Costing")

    subtotal = (

        final_fabric_amount +

        trims_total +

        (cmt_value * order_qty) +

        (fob_value * order_qty)
    )

    commission_percent = st.number_input(
        "Commission %",
        value=2.0
    )

    other_expense_percent = st.number_input(
        "Other Expense %",
        value=3.0
    )

    profit_percent = st.number_input(
        "Profit Margin %",
        value=10.0
    )

    commission_amount = (
        subtotal *
        commission_percent / 100
    )

    other_expense_amount = (
        subtotal *
        other_expense_percent / 100
    )

    profit_amount = (
        subtotal *
        profit_percent / 100
    )

    final_amount = (

        subtotal +

        commission_amount +

        other_expense_amount +

        profit_amount
    )

    cost_per_piece = (
        final_amount /
        order_qty
    )

    # =========================================================
    # FINAL SUMMARY
    # =========================================================

    final_summary = pd.DataFrame([{

        "Subtotal":
        round(subtotal, 2),

        "Commission":
        round(commission_amount, 2),

        "Other Expense":
        round(other_expense_amount, 2),

        "Profit":
        round(profit_amount, 2),

        "Final Amount":
        round(final_amount, 2),

        "Cost / Piece":
        round(cost_per_piece, 2)

    }])

    st.dataframe(
        final_summary,
        use_container_width=True
    )

    st.success(
        f"✅ Final Garment Cost : ₹ {round(cost_per_piece, 2)} / Piece"
    )
    st.markdown("---")

    if st.button("💾 Save Costing"):

        data[style_name] = {

            "Style Name": style_name,

            "Order Qty": order_qty,

            "Avg Piece Weight":
            round(avg_piece_weight, 2),

            "Total Fabric Kg":
            round(total_fabric_kg, 2),

            "Fabric Amount":
            round(final_fabric_amount, 2),

            "Trims Cost":
            round(trims_total, 2),

            "Final Amount":
            round(final_amount, 2),

            "Cost Per Piece":
            round(cost_per_piece, 2)
        }

        save_json(
            FILE,
            data
        )

        st.success(
            "✅ Costing Saved Successfully"
        )
    # =========================================================
    # SAVED COSTINGS
    # =========================================================

    st.markdown("---")

    st.subheader("📂 Saved Costings")

    saved_data = load_json(FILE)

    if saved_data:

        saved_rows = []

        for style, details in saved_data.items():

            saved_rows.append(details)

        saved_df = pd.DataFrame(
            saved_rows
        )

        st.dataframe(
            saved_df,
            use_container_width=True
        )

    else:

        st.info(
            "No Costings Saved Yet"
        )