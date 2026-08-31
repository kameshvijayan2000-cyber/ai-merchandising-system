import streamlit as st
import pandas as pd
from modules.utils import load_json, save_json

FILE = "data/cost_estimator.json"

def run():
    st.header("💰 Cost Estimator")

    # ================= LOAD DATA & SESSION STATE =================
    data = load_json(FILE)
    if not isinstance(data, dict):
        data = {}

    st.markdown("---")

    # =========================================================
    # RECALL SAVED STYLE / SELECTOR
    # =========================================================
    st.subheader("📂 Load Existing Style")
    saved_styles = ["-- Create New --"] + list(data.keys())
    
    selected_style = st.selectbox("Select a Style to Edit/Load", saved_styles)

    # Pre-fill data if a saved style is selected
    style_data = data.get(selected_style, {}) if selected_style != "-- Create New --" else {}

    st.markdown("---")

    # =========================================================
    # BASIC DETAILS
    # =========================================================
    st.subheader("📋 Style Details")

    style_name = st.text_input(
        "Style Name",
        value=style_data.get("Style Name", selected_style if selected_style != "-- Create New --" else ""),
        key="style_name"
    )

    order_qty = st.number_input(
        "Order Quantity",
        min_value=1,
        value=int(style_data.get("Order Qty", 1000)),
        key="order_qty"
    )

    # =========================================================
    # FABRIC EXCESS
    # =========================================================
    st.markdown("---")
    st.subheader("🧵 Fabric Process Qty")

    fabric_excess_percent = st.number_input(
        "Fabric Process Excess %",
        value=float(style_data.get("Fabric Excess %", 7.0)),
        key="fabric_excess_percent"
    )

    final_fabric_qty = order_qty * (1 + fabric_excess_percent / 100)
    st.success(f"Final Fabric Qty : {round(final_fabric_qty, 0)} PCS")

    # =========================================================
    # SIZE INPUT
    # =========================================================
    st.markdown("---")
    st.subheader("📏 Sizes")

    size_input = st.text_input(
        "Enter Sizes",
        value=style_data.get("Sizes", "XS,S,M,L,XL"),
        key="size_input"
    )

    sizes = [x.strip() for x in size_input.split(",") if x.strip()]

    # =========================================================
    # COMPONENTS (GSM TOGGLES)
    # =========================================================
    st.markdown("---")
    
    # Body
    st.subheader("👕 Body")
    include_body = st.checkbox("Include Body", value=style_data.get("Include Body", True), key="inc_body")
    body_gsm = st.number_input("Body GSM", value=float(style_data.get("Body GSM", 220.0)), key="body_gsm") if include_body else 0.0

    # Sleeve
    st.markdown("---")
    st.subheader("🦾 Sleeve")
    include_sleeve = st.checkbox("Include Sleeve", value=style_data.get("Include Sleeve", True), key="inc_sleeve")
    sleeve_gsm = st.number_input("Sleeve GSM", value=float(style_data.get("Sleeve GSM", 220.0)), key="sleeve_gsm") if include_sleeve else 0.0

    # Bottom Rib
    st.markdown("---")
    st.subheader("📏 Bottom Rib")
    include_bottom_rib = st.checkbox("Include Bottom Rib", value=style_data.get("Include Bottom Rib", False), key="inc_bottom_rib")
    bottom_rib_gsm = st.number_input("Bottom Rib GSM", value=float(style_data.get("Bottom Rib GSM", 320.0)), key="bottom_rib_gsm") if include_bottom_rib else 0.0

    # Cuff
    st.markdown("---")
    st.subheader("✋ Hand Cuff")
    include_cuff = st.checkbox("Include Hand Cuff", value=style_data.get("Include Hand Cuff", False), key="inc_cuff")
    cuff_gsm = st.number_input("Cuff GSM", value=float(style_data.get("Cuff GSM", 320.0)), key="cuff_gsm") if include_cuff else 0.0

    # Neck Rib
    st.markdown("---")
    st.subheader("🧣 Neck Rib")
    include_neck = st.checkbox("Include Neck Rib", value=style_data.get("Include Neck Rib", False), key="inc_neck")
    neck_gsm = st.number_input("Neck Rib GSM", value=float(style_data.get("Neck Rib GSM", 320.0)), key="neck_gsm") if include_neck else 0.0

    # Hoodie
    st.markdown("---")
    st.subheader("🧥 Hoodie")
    include_hoodie = st.checkbox("Include Hoodie", value=style_data.get("Include Hoodie", False), key="inc_hoodie")
    hoodie_gsm = st.number_input("Hoodie GSM", value=float(style_data.get("Hoodie GSM", 220.0)), key="hoodie_gsm") if include_hoodie else 0.0

    # =========================================================
    # MEASUREMENTS BY SIZE
    # =========================================================
    st.markdown("---")
    st.subheader("📐 Measurement Inputs")

    piece_rows = []
    saved_measurements = style_data.get("Measurements", {})

    for size in sizes:
        st.markdown("---")
        st.write(f"## Size : {size}")
        total_weight = 0
        size_m = saved_measurements.get(size, {})

        if include_body:
            col1, col2 = st.columns(2)
            with col1:
                body_length = st.number_input(f"{size} Body Length", value=float(size_m.get("body_length", 70.0)), key=f"body_length_{size}")
            with col2:
                body_width = st.number_input(f"{size} Body Width", value=float(size_m.get("body_width", 55.0)), key=f"body_width_{size}")
            total_weight += (body_length * body_width * 2 * body_gsm) / 10000

        if include_sleeve:
            col3, col4 = st.columns(2)
            with col3:
                sleeve_length = st.number_input(f"{size} Sleeve Length", value=float(size_m.get("sleeve_length", 24.0)), key=f"sleeve_length_{size}")
            with col4:
                sleeve_width = st.number_input(f"{size} Sleeve Width", value=float(size_m.get("sleeve_width", 22.0)), key=f"sleeve_width_{size}")
            total_weight += (sleeve_length * sleeve_width * 4 * sleeve_gsm) / 10000

        if include_bottom_rib:
            col5, col6 = st.columns(2)
            with col5:
                bottom_length = st.number_input(f"{size} Bottom Rib Length", value=float(size_m.get("bottom_length", 45.0)), key=f"bottom_length_{size}")
            with col6:
                bottom_width = st.number_input(f"{size} Bottom Rib Width", value=float(size_m.get("bottom_width", 8.0)), key=f"bottom_width_{size}")
            total_weight += (bottom_length * bottom_width * 2 * bottom_rib_gsm) / 10000

        if include_cuff:
            col7, col8 = st.columns(2)
            with col7:
                cuff_length = st.number_input(f"{size} Cuff Length", value=float(size_m.get("cuff_length", 10.0)), key=f"cuff_length_{size}")
            with col8:
                cuff_width = st.number_input(f"{size} Cuff Width", value=float(size_m.get("cuff_width", 8.0)), key=f"cuff_width_{size}")
            total_weight += (cuff_length * cuff_width * 4 * cuff_gsm) / 10000

        if include_neck:
            col9, col10 = st.columns(2)
            with col9:
                neck_length = st.number_input(f"{size} Neck Length", value=float(size_m.get("neck_length", 20.0)), key=f"neck_length_{size}")
            with col10:
                neck_width = st.number_input(f"{size} Neck Width", value=float(size_m.get("neck_width", 5.0)), key=f"neck_width_{size}")
            total_weight += (neck_length * neck_width * 2 * neck_gsm) / 10000

        if include_hoodie:
            col11, col12 = st.columns(2)
            with col11:
                hoodie_length = st.number_input(f"{size} Hoodie Length", value=float(size_m.get("hoodie_length", 35.0)), key=f"hoodie_length_{size}")
            with col12:
                hoodie_width = st.number_input(f"{size} Hoodie Width", value=float(size_m.get("hoodie_width", 30.0)), key=f"hoodie_width_{size}")
            total_weight += (hoodie_length * hoodie_width * 2 * hoodie_gsm) / 10000

        piece_rows.append({"Size": size, "Piece Weight (g)": round(total_weight, 3)})

    # =========================================================
    # DISPLAY PIECE WEIGHT
    # =========================================================
    st.markdown("---")
    st.subheader("📊 Piece Weight Summary")
    piece_df = pd.DataFrame(piece_rows)
    st.dataframe(piece_df, use_container_width=True)

    avg_piece_weight = piece_df["Piece Weight (g)"].mean() if not piece_df.empty else 0.0
    st.success(f"Average Piece Weight : {avg_piece_weight:.2f} g")

    # =========================================================
    # FABRIC CALCULATION
    # =========================================================
    st.markdown("---")
    st.subheader("🧵 Fabric Costing")

    yarn_rate = st.number_input("Yarn Rate / Kg", value=float(style_data.get("Yarn Rate", 280.0)), key="yarn_rate")
    dyeing_rate = st.number_input("Dyeing Rate / Kg", value=float(style_data.get("Dyeing Rate", 80.0)), key="dyeing_rate")
    compacting_rate = st.number_input("Compacting Rate / Kg", value=float(style_data.get("Compacting Rate", 25.0)), key="compacting_rate")
    washing_rate = st.number_input("Washing Rate / Kg", value=float(style_data.get("Washing Rate", 20.0)), key="washing_rate")

    # Additional Processes
    st.markdown("---")
    st.subheader("➕ Additional Fabric Processes")
    process_count = st.number_input("No of Additional Processes", min_value=0, value=int(style_data.get("Process Count", 0)), key="process_count")
    
    extra_process_total = 0
    saved_processes = style_data.get("Extra Processes", [])
    for i in range(process_count):
        col13, col14 = st.columns(2)
        p_name_val = saved_processes[i]["name"] if i < len(saved_processes) else ""
        p_rate_val = saved_processes[i]["rate"] if i < len(saved_processes) else 0.0
        
        with col13:
            p_name = st.text_input(f"Process Name {i+1}", value=p_name_val, key=f"process_name_{i}")
        with col14:
            p_rate = st.number_input(f"{p_name if p_name else f'Process {i+1}'} Rate", value=float(p_rate_val), key=f"process_rate_{i}")
        extra_process_total += p_rate

    # Fabric Loss
    fabric_loss_percent = st.number_input("Fabric Loss %", value=float(style_data.get("Fabric Loss %", 5.0)), key="fabric_loss_percent")

    base_fabric_kg = (avg_piece_weight * final_fabric_qty) / 1000
    total_fabric_kg = base_fabric_kg * (1 + fabric_loss_percent / 100)
    fabric_rate = yarn_rate + dyeing_rate + compacting_rate + washing_rate + extra_process_total
    final_fabric_amount = total_fabric_kg * fabric_rate

    # Fabric Summary
    st.markdown("---")
    st.subheader("🧵 Fabric Summary")
    fabric_summary = pd.DataFrame([{
        "Final Fabric Qty": round(final_fabric_qty, 0),
        "Avg Piece Weight (g)": round(avg_piece_weight, 2),
        "Total Fabric (Kg)": round(total_fabric_kg, 2),
        "Fabric Rate / Kg": round(fabric_rate, 2),
        "Fabric Amount": round(final_fabric_amount, 2)
    }])
    st.dataframe(fabric_summary, use_container_width=True)

    # =========================================================
    # TRIMS
    # =========================================================
    st.markdown("---")
    st.subheader("🎀 Trims & Accessories")

    trims_excess_percent = st.number_input("Trims Excess %", value=float(style_data.get("Trims Excess %", 5.0)), key="trims_excess_percent")
    trims_qty = order_qty * (1 + trims_excess_percent / 100)

    trim_count = st.number_input("Number of Trims", min_value=1, value=int(style_data.get("Trim Count", 1)), key="trim_count")

    trim_rows = []
    trims_total = 0
    saved_trims = style_data.get("Trims Detail", [])

    for i in range(trim_count):
        col15, col16 = st.columns(2)
        t_name_val = saved_trims[i]["name"] if i < len(saved_trims) else ""
        t_rate_val = saved_trims[i]["rate"] if i < len(saved_trims) else 0.0

        with col15:
            trim_name = st.text_input(f"Trim Name {i+1}", value=t_name_val, key=f"trim_name_{i}")
        with col16:
            trim_rate = st.number_input(f"{trim_name if trim_name else f'Trim {i+1}'} Rate", value=float(t_rate_val), key=f"trim_rate_{i}")

        trim_amount = trims_qty * trim_rate
        trims_total += trim_amount
        trim_rows.append({"Trim": trim_name, "Rate": trim_rate, "Amount": round(trim_amount, 2)})

    st.dataframe(pd.DataFrame(trim_rows), use_container_width=True)
    st.success(f"Total Trims Cost : ₹ {round(trims_total, 2)}")

    # =========================================================
    # OTHER COSTS & FINAL CALCULATION
    # =========================================================
    st.markdown("---")
    st.subheader("🏭 Other Costs")

    cmt_value = st.number_input("CMT Value", value=float(style_data.get("CMT Value", 50.0)), key="cmt_value")
    fob_value = st.number_input("FOB Charges", value=float(style_data.get("FOB Value", 20.0)), key="fob_value")

    st.markdown("---")
    st.subheader("📈 Final Costing")

    subtotal = final_fabric_amount + trims_total + (cmt_value * order_qty) + (fob_value * order_qty)

    commission_percent = st.number_input("Commission %", value=float(style_data.get("Commission %", 2.0)), key="commission_percent")
    other_expense_percent = st.number_input("Other Expense %", value=float(style_data.get("Other Expense %", 3.0)), key="other_expense_percent")
    profit_percent = st.number_input("Profit Margin %", value=float(style_data.get("Profit Margin %", 10.0)), key="profit_percent")

    commission_amount = subtotal * commission_percent / 100
    other_expense_amount = subtotal * other_expense_percent / 100
    profit_amount = subtotal * profit_percent / 100

    final_amount = subtotal + commission_amount + other_expense_amount + profit_amount
    cost_per_piece = final_amount / order_qty if order_qty > 0 else 0

    final_summary = pd.DataFrame([{
        "Subtotal": round(subtotal, 2),
        "Commission": round(commission_amount, 2),
        "Other Expense": round(other_expense_amount, 2),
        "Profit": round(profit_amount, 2),
        "Final Amount": round(final_amount, 2),
        "Cost / Piece": round(cost_per_piece, 2)
    }])
    st.dataframe(final_summary, use_container_width=True)

    st.success(f"✅ Final Garment Cost : ₹ {round(cost_per_piece, 2)} / Piece")
    st.markdown("---")

    # =========================================================
    # SAVE ACTION
    # =========================================================
    if st.button("💾 Save Costing"):
        if not style_name.strip():
            st.error("Please enter a valid Style Name before saving.")
            return

        # Build detailed measurement map
        measurements_to_save = {}
        for sz in sizes:
            measurements_to_save[sz] = {
                "body_length": st.session_state.get(f"body_length_{sz}", 70.0),
                "body_width": st.session_state.get(f"body_width_{sz}", 55.0),
                "sleeve_length": st.session_state.get(f"sleeve_length_{sz}", 24.0),
                "sleeve_width": st.session_state.get(f"sleeve_width_{sz}", 22.0),
                "bottom_length": st.session_state.get(f"bottom_length_{sz}", 45.0),
                "bottom_width": st.session_state.get(f"bottom_width_{sz}", 8.0),
                "cuff_length": st.session_state.get(f"cuff_length_{sz}", 10.0),
                "cuff_width": st.session_state.get(f"cuff_width_{sz}", 8.0),
                "neck_length": st.session_state.get(f"neck_length_{sz}", 20.0),
                "neck_width": st.session_state.get(f"neck_width_{sz}", 5.0),
                "hoodie_length": st.session_state.get(f"hoodie_length_{sz}", 35.0),
                "hoodie_width": st.session_state.get(f"hoodie_width_{sz}", 30.0),
            }

        # Structure full object to reload later
        data[style_name] = {
            "Style Name": style_name,
            "Order Qty": order_qty,
            "Fabric Excess %": fabric_excess_percent,
            "Sizes": size_input,
            "Include Body": include_body,
            "Body GSM": body_gsm,
            "Include Sleeve": include_sleeve,
            "Sleeve GSM": sleeve_gsm,
            "Include Bottom Rib": include_bottom_rib,
            "Bottom Rib GSM": bottom_rib_gsm,
            "Include Cuff": include_cuff,
            "Cuff GSM": cuff_gsm,
            "Include Neck": include_neck,
            "Neck GSM": neck_gsm,
            "Include Hoodie": include_hoodie,
            "Hoodie GSM": hoodie_gsm,
            "Measurements": measurements_to_save,
            "Yarn Rate": yarn_rate,
            "Dyeing Rate": dyeing_rate,
            "Compacting Rate": compacting_rate,
            "Washing Rate": washing_rate,
            "Process Count": process_count,
            "Extra Processes": [{"name": st.session_state.get(f"process_name_{i}", ""), "rate": st.session_state.get(f"process_rate_{i}", 0.0)} for i in range(process_count)],
            "Fabric Loss %": fabric_loss_percent,
            "Trims Excess %": trims_excess_percent,
            "Trim Count": trim_count,
            "Trims Detail": [{"name": st.session_state.get(f"trim_name_{i}", ""), "rate": st.session_state.get(f"trim_rate_{i}", 0.0)} for i in range(trim_count)],
            "CMT Value": cmt_value,
            "FOB Value": fob_value,
            "Commission %": commission_percent,
            "Other Expense %": other_expense_percent,
            "Profit Margin %": profit_percent,
            "Avg Piece Weight": round(avg_piece_weight, 2),
            "Total Fabric Kg": round(total_fabric_kg, 2),
            "Fabric Amount": round(final_fabric_amount, 2),
            "Trims Cost": round(trims_total, 2),
            "Final Amount": round(final_amount, 2),
            "Cost Per Piece": round(cost_per_piece, 2)
        }

        save_json(FILE, data)
        st.success(f"✅ Costing for '{style_name}' saved successfully!")
        st.rerun()

    # =========================================================
    # SAVED COSTINGS TABLE
    # =========================================================
    st.markdown("---")
    st.subheader("📂 Saved Costings Overview")
    saved_data = load_json(FILE)

    if saved_data:
        saved_rows = [details for _, details in saved_data.items()]
        st.dataframe(pd.DataFrame(saved_rows), use_container_width=True)
    else:
        st.info("No Costings Saved Yet")