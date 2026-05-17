import streamlit as st
import pandas as pd
import math
from modules.utils import load_json, save_json

MASTER_FILE = "data/style_master.json"
COUNT_FILE = "data/count_data.json"


def count_calculator_module():

    st.header("📦 Count Calculator")

    masters = load_json(MASTER_FILE)

    if not masters:

        st.warning(
            "No styles found. Please create style first."
        )

        return

    count_data = load_json(COUNT_FILE)

    # ================= STYLE =================
    selected_style = st.selectbox(
        "Select Style",
        list(masters.keys())
    )

    master = masters[selected_style]

    total_qty = master["total_qty"]

    extra_percent_master = master.get(
        "extra_percent",
        5.0
    )

    cut_qty_percent = master.get(
        "cut_qty_percent",
        0
    )

    color_ratios = master[
        "color_ratios"
    ]

    # ================= STYLE INFO =================
    st.subheader("📋 Style Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Order Qty",
            total_qty
        )

    with col2:

        st.metric(
            "Pack Extra %",
            extra_percent_master
        )

    with col3:

        st.metric(
            "Cut Qty %",
            cut_qty_percent
        )

    # ================= RATIO DISPLAY =================
    rows = []

    for color, ratios in color_ratios.items():

        row = {"Color": color}

        row.update(ratios)

        rows.append(row)

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )

    # ================= INPUTS =================
    st.markdown("---")

    st.subheader("📦 Carton Planning")

    # ================= LOAD OLD INPUTS =================
    old_inputs = {}

    if (
        selected_style in count_data and
        isinstance(
            count_data[selected_style],
            dict
        ) and
        "inputs" in count_data[
            selected_style
        ]
    ):

        old_inputs = count_data[
            selected_style
        ]["inputs"]

    cartons = st.number_input(
        "Cartons",
        min_value=1,
        value=int(
            old_inputs.get(
                "cartons",
                250
            )
        )
    )

    pcs_per_carton = st.number_input(
        "PCS Per Carton",
        min_value=1,
        value=int(
            old_inputs.get(
                "pcs_per_carton",
                12
            )
        )
    )

    extra_percent = st.number_input(
        "Extra %",
        value=float(
            old_inputs.get(
                "extra_percent",
                extra_percent_master
            )
        )
    )

    # ================= CALCULATIONS =================
    base_qty = cartons * pcs_per_carton

    extra_cartons = math.ceil(
        cartons *
        (extra_percent / 100)
    )

    final_cartons = (
        cartons +
        extra_cartons
    )

    st.markdown("---")

    col4, col5, col6 = st.columns(3)

    with col4:

        st.info(
            f"Base Qty : {base_qty}"
        )

    with col5:

        st.info(
            f"Extra Cartons : {extra_cartons}"
        )

    with col6:

        st.success(
            f"Final Cartons : {final_cartons}"
        )

    # ================= GENERATE =================
    if st.button("🚀 Calculate"):

        result_rows = []

        summary_rows = []

        grand_total = 0

        # ================= COLOR LOOP =================
        for color, ratios in color_ratios.items():

            color_total = 0

            color_ratio_total = sum(
                ratios.values()
            )

            # ================= SIZE LOOP =================
            for size, ratio in ratios.items():

                qty = (
                    final_cartons *
                    ratio
                )

                color_total += qty

                grand_total += qty

                result_rows.append({

                    "Color": color,

                    "Size": size,

                    "Ratio": ratio,

                    "Qty": int(qty)
                })

            # ================= SUMMARY =================
            summary_rows.append({

                "Color": color,

                "Color Ratio Total":
                color_ratio_total,

                "Total Qty":
                int(color_total)
            })

        # ================= DATAFRAMES =================
        detail_df = pd.DataFrame(
            result_rows
        )

        summary_df = pd.DataFrame(
            summary_rows
        )

        # ================= DISPLAY =================
        st.subheader(
            "📊 Size-wise Breakdown"
        )

        st.dataframe(
            detail_df,
            use_container_width=True
        )

        st.metric(
            "📦 Total Order Qty",
            int(grand_total)
        )

        st.subheader(
            "🎨 Color Summary"
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # ================= GRAND SUMMARY =================
        grand_summary = pd.DataFrame([{

            "Total Colors":
            len(summary_df),

            "Total Cartons":
            final_cartons,

            "Grand Total Qty":
            int(grand_total)

        }])

        st.subheader(
            "📦 Grand Summary"
        )

        st.dataframe(
            grand_summary,
            use_container_width=True
        )

        # ================= SAVE =================
        count_data[selected_style] = {

            "results":
            result_rows,

            "summary":
            summary_rows,

            "inputs": {

                "cartons":
                cartons,

                "pcs_per_carton":
                pcs_per_carton,

                "extra_percent":
                extra_percent,

                "final_cartons":
                final_cartons
            }
        }

        save_json(
            COUNT_FILE,
            count_data
        )

        st.success(
            "✅ Count Saved Successfully"
        )

    # ================= OLD DATA =================
    st.markdown("---")

    if selected_style in count_data:

        st.subheader(
            "📂 Existing Count Data"
        )

        old_data = count_data[
            selected_style
        ]

        # ================= OLD FORMAT =================
        if isinstance(old_data, list):

            old_df = pd.DataFrame(
                old_data
            )

            st.dataframe(
                old_df,
                use_container_width=True
            )

        # ================= NEW FORMAT =================
        elif isinstance(old_data, dict):

            # ===== RESULTS =====
            if "results" in old_data:

                old_df = pd.DataFrame(
                    old_data["results"]
                )

                st.dataframe(
                    old_df,
                    use_container_width=True
                )

            # ===== SUMMARY =====
            if "summary" in old_data:

                st.subheader(
                    "🎨 Saved Color Summary"
                )

                old_summary = pd.DataFrame(
                    old_data["summary"]
                )

                st.dataframe(
                    old_summary,
                    use_container_width=True
                )

    # ================= ALL STYLE SUMMARY =================
    st.markdown("---")

    st.subheader(
        "📦 All Styles Count Summary"
    )

    all_rows = []

    for style, data in count_data.items():

        if (
            isinstance(data, dict) and
            "summary" in data
        ):

            temp_df = pd.DataFrame(
                data["summary"]
            )

            temp_df["Style"] = style

            all_rows.append(temp_df)

    if all_rows:

        final_df = pd.concat(
            all_rows,
            ignore_index=True
        )

        st.dataframe(
            final_df,
            use_container_width=True
        )

        total_summary = pd.DataFrame([{

            "Total Styles":
            final_df["Style"].nunique(),

            "Grand Total Qty":
            int(
                final_df[
                    "Total Qty"
                ].sum()
            )

        }])

        st.subheader(
            "📊 Overall Summary"
        )

        st.dataframe(
            total_summary,
            use_container_width=True
        )

    # ================= CLEAR =================
    st.markdown("---")

    if st.button(
        "🗑️ Clear Current Style Count Data"
    ):

        if selected_style in count_data:

            del count_data[
                selected_style
            ]

            save_json(
                COUNT_FILE,
                count_data
            )

            st.success(
                f"{selected_style} data cleared"
            )

            st.rerun()