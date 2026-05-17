import streamlit as st
import pandas as pd
from modules.utils import load_json, save_json

MASTER_FILE = "data/style_master.json"
FABRIC_FILE = "data/fabric_program.json"


# ================= MAIN =================
def run():

    st.header("🧵 Fabric Program")

    masters = load_json(MASTER_FILE)

    if not masters:

        st.warning(
            "No styles found. Please create style first."
        )

        return

    fabric_data = load_json(FABRIC_FILE)

    # ================= STYLE =================
    selected_style = st.selectbox(
        "Select Style",
        list(masters.keys())
    )

    master = masters[selected_style]

    total_qty = master["total_qty"]

    # 🔥 CUTTING EXTRA %
    cut_qty_percent = master.get(
        "cut_qty_percent",
        0
    )

    # 🔥 PACK EXTRA %
    extra_percent = master.get(
        "extra_percent",
        0
    )

    color_ratios = master["color_ratios"]

    # ================= SHOW STYLE =================
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
            extra_percent
        )

    with col3:

        st.metric(
            "Cut Qty %",
            cut_qty_percent
        )

    rows = []

    for color, ratios in color_ratios.items():

        row = {"Color": color}

        row.update(ratios)

        rows.append(row)

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )

    # ================= FABRIC INPUTS =================
    st.markdown("---")

    st.subheader("⚖️ Fabric Inputs")

    # ================= LOAD OLD INPUTS =================
    old_inputs = {}

    if (
        selected_style in fabric_data and
        "inputs" in fabric_data[selected_style]
    ):

        old_inputs = fabric_data[
            selected_style
        ]["inputs"]

    body_weight = st.number_input(
        "Body Weight",
        value=float(
            old_inputs.get(
                "body_weight",
                0.350
            )
        ),
        format="%.3f"
    )

    rib_weight = st.number_input(
        "Rib Weight",
        value=float(
            old_inputs.get(
                "rib_weight",
                0.100
            )
        ),
        format="%.3f"
    )

    sj_weight = st.number_input(
        "SJ Weight",
        value=float(
            old_inputs.get(
                "sj_weight",
                0.003
            )
        ),
        format="%.3f"
    )

    body_loss = st.number_input(
        "Body Loss %",
        value=float(
            old_inputs.get(
                "body_loss",
                13.0
            )
        )
    )

    rib_loss = st.number_input(
        "Rib Loss %",
        value=float(
            old_inputs.get(
                "rib_loss",
                10.0
            )
        )
    )

    sj_loss = st.number_input(
        "SJ Loss %",
        value=float(
            old_inputs.get(
                "sj_loss",
                0.0
            )
        )
    )

    # ================= GENERATE =================
    if st.button("🚀 Generate Fabric"):

        results = []

        # TOTAL RATIO
        total_ratio_units = sum(
            sum(v.values())
            for v in color_ratios.values()
        )

        # BASE PCS
        base_qty = (
            total_qty /
            total_ratio_units
        )

        for color, sizes in color_ratios.items():

            body_total = 0
            rib_total = 0
            sj_total = 0

            color_order_qty = 0

            # COLOR RATIO TOTAL
            color_ratio_total = sum(
                sizes.values()
            )

            # COLOR ORDER QTY
            color_qty = (
                base_qty *
                color_ratio_total
            )

            # CUTTING EXTRA
            color_qty = color_qty * (
                1 + cut_qty_percent / 100
            )

            color_order_qty = round(
                color_qty,
                0
            )

            # SIZE CALCULATION
            for size, ratio in sizes.items():

                size_qty = (
                    color_qty /
                    color_ratio_total
                ) * ratio

                # BODY
                body_total += (
                    size_qty *
                    body_weight *
                    (1 + body_loss / 100)
                )

                # RIB
                rib_total += (
                    size_qty *
                    rib_weight *
                    (1 + rib_loss / 100)
                )

                # SJ
                sj_total += (
                    size_qty *
                    sj_weight *
                    (1 + sj_loss / 100)
                )

            results.append({

                "Color": color,

                "Order Qty": round(
                    color_order_qty,
                    0
                ),

                "Body Total (Kg)": round(
                    body_total,
                    2
                ),

                "Rib Total (Kg)": round(
                    rib_total,
                    2
                ),

                "SJ Total (Kg)": round(
                    sj_total,
                    2
                ),

                "Grand Total (Kg)": round(
                    body_total +
                    rib_total +
                    sj_total,
                    2
                )
            })

        df = pd.DataFrame(results)

        # ================= DISPLAY =================
        st.subheader("📊 Fabric Requirement")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ================= TOTAL SUMMARY =================
        total_body = df[
            "Body Total (Kg)"
        ].sum()

        total_rib = df[
            "Rib Total (Kg)"
        ].sum()

        total_sj = df[
            "SJ Total (Kg)"
        ].sum()

        total_grand = df[
            "Grand Total (Kg)"
        ].sum()

        summary_df = pd.DataFrame([{

            "Total Body (Kg)": round(
                total_body,
                2
            ),

            "Total Rib (Kg)": round(
                total_rib,
                2
            ),

            "Total SJ (Kg)": round(
                total_sj,
                2
            ),

            "Grand Total (Kg)": round(
                total_grand,
                2
            )

        }])

        st.subheader(
            "📦 Style Total Summary"
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # ================= SAVE =================
        fabric_data[selected_style] = {

            "results": results,

            "inputs": {

                "body_weight": body_weight,

                "rib_weight": rib_weight,

                "sj_weight": sj_weight,

                "body_loss": body_loss,

                "rib_loss": rib_loss,

                "sj_loss": sj_loss
            }
        }

        save_json(
            FABRIC_FILE,
            fabric_data
        )

        st.success(
            "✅ Fabric Saved Successfully"
        )

    # ================= VIEW SAVED =================
    st.markdown("---")

    if selected_style in fabric_data:

        st.subheader(
            "📂 Existing Fabric Data"
        )

        old_df = pd.DataFrame(
            fabric_data[selected_style][
                "results"
            ]
        )

        st.dataframe(
            old_df,
            use_container_width=True
        )

    # ================= GRAND SUMMARY =================
    st.markdown("---")

    st.subheader(
        "📦 All Styles Fabric Summary"
    )

    all_rows = []

    for style, data in fabric_data.items():

        if "results" not in data:
            continue

        temp_df = pd.DataFrame(
            data["results"]
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

        # ================= GRAND TOTAL =================
        summary_df = pd.DataFrame([{

            "Body Total (Kg)": round(
                final_df[
                    "Body Total (Kg)"
                ].sum(),
                2
            ),

            "Rib Total (Kg)": round(
                final_df[
                    "Rib Total (Kg)"
                ].sum(),
                2
            ),

            "SJ Total (Kg)": round(
                final_df[
                    "SJ Total (Kg)"
                ].sum(),
                2
            ),

            "Grand Total (Kg)": round(
                final_df[
                    "Grand Total (Kg)"
                ].sum(),
                2
            )

        }])

        st.subheader(
            "📊 Grand Total Summary"
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

    # ================= CLEAR CURRENT STYLE =================
    st.markdown("---")

    if st.button(
        "🗑️ Clear Current Style Fabric Data"
    ):

        if selected_style in fabric_data:

            del fabric_data[selected_style]

            save_json(
                FABRIC_FILE,
                fabric_data
            )

            st.success(
                f"{selected_style} data cleared"
            )

            st.rerun()