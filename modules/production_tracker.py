import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date
from modules.utils import load_json, save_json

FILE = "data/production_tracking.json"
COUNT_FILE = "data/count_data.json"
STYLE_FILE = "data/style_master.json"


def run():

    st.header("🏭 Production Tracker")

    # =========================================================
    # LOAD DATA
    # =========================================================

    data = load_json(FILE)

    count_data = load_json(COUNT_FILE)
    masters = load_json(STYLE_FILE)

    # =========================================================
    # INITIALIZE
    # =========================================================

    if "entries" not in data:
        data["entries"] = []

    # =========================================================
    # PROCESS LIST
    # =========================================================

    garment_processes = [

        "Cutting",
        "Stitching",
        "Checking",
        "Ironing",
        "Packing"

    ]

    # =========================================================
    # ADD ENTRY
    # =========================================================

    st.subheader("➕ Add Production Entry")
    
    # ================= PO SELECT =================

    po_list = sorted(

        list(

            set(

                details.get(
                    "po_number",
                    "N/A"
                )

                for details in masters.values()
            )

        )
    )

    selected_po = st.selectbox(
        "Select PO Number",
        po_list
    )

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

    # =========================================================
    # DATE
    # =========================================================

    entry_date = st.date_input(
        "Date",
        value=date.today()
    )

    # =========================================================
    # GARMENT PROCESS
    # =========================================================

    if process in garment_processes:

        # =====================================================
        # CHECK COUNT DATA
        # =====================================================

        if not count_data:

            st.warning(
                "No Count Calculator Data Found"
            )

            return

        # =====================================================
        # STYLE SELECT
        # =====================================================

        filtered_styles = []

        for key in count_data.keys():

            if key.startswith(
                f"{selected_po}_"
            ):

                filtered_styles.append(key)

        if not filtered_styles:

            st.warning(
                "No Count Data Found For This PO"
            )

            return

        style = st.selectbox(

            "Select Style",

            filtered_styles
        )

        style_data = count_data[style]

        result_data = style_data.get(
            "results",
            []
        )

        result_df = pd.DataFrame(
            result_data
        )

        if result_df.empty:

            st.warning(
                "No Count Data Available"
            )

            return

        # =====================================================
        # COLOR SELECT
        # =====================================================

        colors = result_df[
            "Color"
        ].unique().tolist()

        selected_color = st.selectbox(
            "Select Color",
            colors
        )

        # =====================================================
        # FILTER COLOR
        # =====================================================

        color_df = result_df[

            result_df["Color"] ==
            selected_color

        ]

        # =====================================================
        # SIZE SELECT
        # =====================================================

        sizes = color_df[
            "Size"
        ].unique().tolist()

        selected_size = st.selectbox(
            "Select Size",
            sizes
        )

        # =====================================================
        # TARGET QTY
        # =====================================================

        target_row = color_df[

            color_df["Size"] ==
            selected_size

        ]

        target_qty = int(
            target_row.iloc[0]["Qty"]
        )

        # =====================================================
        # OLD COMPLETED
        # =====================================================

        old_completed = 0

        for row in data["entries"]:

            if (

                row.get("Process") == process
                and
                row.get("Style") == style
                and
                row.get("Color") == selected_color
                and
                row.get("Size") == selected_size

            ):

                old_completed += row.get(
                    "Completed Qty",
                    0
                )

        # =====================================================
        # CURRENT ENTRY
        # =====================================================

        completed_qty = st.number_input(

            f"{process} Completed Qty",

            min_value=0,

            value=0
        )
        # ==========================================
        # CUTTING PART
        # ==========================================
        cutting_part = ""

        if process == "Cutting":

            cutting_part = st.text_input(
                "Cutting Part (Body / Sleeve / Hood / Rib / Pocket etc.)"
            )
        # =====================================================
        # BALANCE
        # =====================================================

        total_completed = (
            old_completed +
            completed_qty
        )

        balance_qty = (
            target_qty -
            total_completed
        )

        if balance_qty < 0:
            balance_qty = 0

        # =====================================================
        # PARTY & RATE
        # =====================================================

        col1, col2 = st.columns(2)

        with col1:

            party = st.text_input(
                "Party / Unit"
            )

        with col2:

            rate = st.number_input(
                "Rate",
                min_value=0.0,
                format="%.2f"
            )

        total = completed_qty * rate

        # =====================================================
        # LIVE SUMMARY
        # =====================================================

        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.info(
                f"Target Qty : {target_qty}"
            )

        with c2:

            st.success(
                f"Already Completed : {old_completed}"
            )

        with c3:

            st.warning(
                f"Current Entry : {completed_qty}"
            )

        with c4:

            st.error(
                f"Balance : {balance_qty}"
            )

        st.success(
            f"💰 Total Cost : ₹ {round(total,2)}"
        )

        # =====================================================
        # SAVE ENTRY
        # =====================================================

        if st.button("💾 Save Entry"):

            data["entries"].append({
                
                "PO Number":
                selected_po,

                "Date":
                str(entry_date),

                "Process":
                process,

                "Style":
                style,

                "Color":
                selected_color,

                "Size":
                selected_size,

                "Cutting Part":
                cutting_part,
                
                "Target Qty":
                target_qty,

                "Completed Qty":
                completed_qty,

                "Balance":
                balance_qty,

                "Party":
                party,

                "Rate":
                rate,

                "Total":
                total
            })

            save_json(FILE, data)

            st.success(
                "✅ Entry Saved Successfully"
            )

            st.rerun()

    # =========================================================
    # OTHER PROCESS
    # =========================================================

    else:

        col3, col4 = st.columns(2)

        with col3:

            entry_type = st.selectbox(
                "Type",
                ["Input", "Output"]
            )

            qty = st.number_input(
                "Qty",
                min_value=0.0,
                format="%.2f"
            )

        with col4:

            party = st.text_input(
                "Party / Unit"
            )

            rate = st.number_input(
                "Rate",
                min_value=0.0,
                format="%.2f"
            )

        description = st.text_input(
            "Description"
        )

        total = qty * rate

        st.success(
            f"💰 Total Cost : ₹ {round(total,2)}"
        )

        # =====================================================
        # SAVE
        # =====================================================

        if st.button("💾 Save Entry"):

            data["entries"].append({
                
                "PO Number":
                selected_po,

                "Date":
                str(entry_date),

                "Process":
                process,

                "Type":
                entry_type,

                "Qty":
                qty,

                "Party":
                party,

                "Description":
                description,

                "Rate":
                rate,

                "Total":
                total
            })

            save_json(FILE, data)

            st.success(
                "✅ Entry Saved Successfully"
            )

            st.rerun()

    # =========================================================
    # DISPLAY DATA & IN-ROW DELETE
    # =========================================================

    st.markdown("---")

    st.subheader("📊 Production Entries")

    # View Mode Selection: Consolidated or Single PO
    view_mode = st.radio(
        "Select View Type:",
        ["Single PO View", "All POs (Consolidated)"],
        horizontal=True
    )

    # Filter entries based on selected view mode
    if view_mode == "Single PO View":
        display_entries = [
            (idx, entry)
            for idx, entry in enumerate(data["entries"])
            if entry.get("PO Number") == selected_po
        ]
    else:
        display_entries = [
            (idx, entry)
            for idx, entry in enumerate(data["entries"])
        ]

    if display_entries:

        # Extract DataFrame for Excel export
        df = pd.DataFrame([e for _, e in display_entries])

        # =====================================================
        # EXCEL DOWNLOAD BUTTON
        # =====================================================
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Production Data")

        file_label = f"Production_Tracker_{selected_po}.xlsx" if view_mode == "Single PO View" else "Production_Tracker_Consolidated.xlsx"

        st.download_button(
            label="📥 Download Excel",
            data=buffer.getvalue(),
            file_name=file_label,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")

        # Header columns
        cols = st.columns([1, 2, 2, 2, 1, 1, 2, 3, 1, 1, 1])

        cols[0].markdown("**#**")
        cols[1].markdown("**PO Number**")
        cols[2].markdown("**Date**")
        cols[3].markdown("**Process**")
        cols[4].markdown("**Type**")
        cols[5].markdown("**Qty**")
        cols[6].markdown("**Party**")
        cols[7].markdown("**Description**")
        cols[8].markdown("**Rate**")
        cols[9].markdown("**Total**")
        cols[10].markdown("**Action**")

        st.markdown("---")

        for row_num, (orig_idx, entry) in enumerate(display_entries, 1):

            c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 = st.columns(
                [1, 2, 2, 2, 1, 1, 2, 3, 1, 1, 1]
            )

            c1.write(str(row_num))
            c2.write(str(entry.get("PO Number", "")))
            c3.write(str(entry.get("Date", "")))
            c4.write(str(entry.get("Process", "")))
            c5.write(str(entry.get("Type", "-")))
            c6.write(str(entry.get("Qty", entry.get("Completed Qty", "-"))))
            c7.write(str(entry.get("Party", "")))
            c8.write(str(entry.get("Description", entry.get("Cutting Part", ""))))
            c9.write(str(entry.get("Rate", "")))
            c10.write(str(entry.get("Total", "")))

            # Delete button directly inside the row's last column
            if c11.button("🗑️", key=f"del_{orig_idx}"):

                data["entries"].pop(orig_idx)

                save_json(FILE, data)

                st.success("Entry Deleted Successfully")

                st.rerun()

        # =====================================================
        # METRICS
        # =====================================================

        st.markdown("---")

        total_entries = len(df)

        total_cost = round(
            df["Total"].sum(),
            2
        )

        total_process = df[
            "Process"
        ].nunique()

        col5, col6, col7 = st.columns(3)

        with col5:

            st.metric(
                "📋 Entries",
                total_entries
            )

        with col6:

            st.metric(
                "🏭 Processes",
                total_process
            )

        with col7:

            st.metric(
                "💰 Total Cost",
                f"₹ {total_cost}"
            )

        # =====================================================
        # GARMENT PROCESS SUMMARY
        # =====================================================

        st.markdown("---")

        st.subheader(
            "📦 Garment Process Summary"
        )

        garment_rows = []

        garment_df = df[

            df["Process"].isin(
                garment_processes
            )

        ]

        if not garment_df.empty:

            grouped = garment_df.groupby([

                "Process",
                "Style",
                "Color",
                "Size"

            ])

            for keys, group in grouped:

                process_name = keys[0]
                style_name = keys[1]
                color_name = keys[2]
                size_name = keys[3]

                # =============================================
                # SAFE HANDLING
                # =============================================

                if "Target Qty" in group.columns:

                    target_qty = group[
                        "Target Qty"
                    ].max()

                else:

                    target_qty = 0

                if "Completed Qty" in group.columns:

                    completed_qty = group[
                        "Completed Qty"
                    ].sum()

                else:

                    completed_qty = 0

                balance_qty = (
                    target_qty -
                    completed_qty
                )

                if balance_qty < 0:
                    balance_qty = 0

                cutting_part_value = ""

                if "Cutting Part" in group.columns:

                    cutting_part_value = (
                        group["Cutting Part"]
                        .fillna("")
                        .iloc[0]
                    )

                garment_rows.append({

                    "Process":
                    process_name,

                    "Style":
                    style_name,

                    "Color":
                    color_name,

                    "Size":
                    size_name,

                    "Cutting Part":
                    cutting_part_value,

                    "Target Qty":
                    target_qty,

                    "Completed":
                    completed_qty,

                    "Balance":
                    balance_qty
                })

            garment_summary_df = pd.DataFrame(
                garment_rows
            )

            st.dataframe(
                garment_summary_df,
                use_container_width=True
            )

        # =====================================================
        # FABRIC PROCESS SUMMARY
        # =====================================================

        st.markdown("---")

        st.subheader(
            "🧵 Fabric Process Summary"
        )

        normal_df = df[

            ~df["Process"].isin(
                garment_processes
            )

        ]

        if not normal_df.empty:

            summary = []

            for p in normal_df["Process"].unique():

                process_df = normal_df[

                    normal_df["Process"] == p

                ]

                if "Type" in process_df.columns:

                    input_qty = process_df[

                        process_df["Type"] == "Input"

                    ]["Qty"].sum()

                    output_qty = process_df[

                        process_df["Type"] == "Output"

                    ]["Qty"].sum()

                else:

                    input_qty = 0
                    output_qty = 0

                balance = (
                    input_qty -
                    output_qty
                )

                summary.append({

                    "Process":
                    p,

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

    else:

        st.info(
            "No Production Entries Added"
        )

    # =========================================================
    # CLEAR DATA
    # =========================================================

    st.markdown("---")

    st.warning(
        "⚠️ This will permanently delete all production tracking data"
    )

    if st.button(
        "🗑️ Clear Production Data"
    ):

        data["entries"] = []

        save_json(
            FILE,
            data
        )

        st.success(
            "All Production Data Cleared"
        )

        st.rerun()