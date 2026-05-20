import streamlit as st
import pandas as pd
from modules.utils import load_json, save_json

FILE = "data/style_master.json"


def run():

    st.header("📋 Style Master Entry")

    # ================= LOAD DATA =================
    data = load_json(FILE)

    # ================= FIX EMPTY =================
    if not isinstance(data, dict):

        data = {}

    # ================= INPUTS =================
    style_name = st.text_input("Style Name")

    total_qty = st.number_input(
        "Total Qty",
        min_value=1,
        value=1000
    )

    # ================= CARTON DETAILS =================
    col_ctn1, col_ctn2 = st.columns(2)

    with col_ctn1:

        cartons = st.number_input(
            "No of Cartons",
            min_value=1,
            value=250
        )

    with col_ctn2:

        pcs_per_carton = st.number_input(
            "PCS Per Carton",
            min_value=1,
            value=12
        )

    # ================= PACK EXTRA =================
    extra_percent = st.number_input(
        "Extra Qty % (For Count Calculator / Packing)",
        value=5.0
    )

    # ================= CUT EXTRA =================
    cut_qty_percent = st.number_input(
        "Cut Qty % (For Fabric Program)",
        value=3.0
    )

    # ================= SIZE INPUT =================
    sizes = st.text_input(
        "Sizes",
        value="XS,S,M,L,XL"
    )

    # ================= COLOR INPUT =================
    colors = st.text_input(
        "Colors",
        value="BLACK,WHITE"
    )

    # ================= RATIOS =================
    ratio_input = st.text_area(
        "Enter Ratios\nExample:\nBLACK=1,1,2,1,1\nWHITE=1,2,2,1,1"
    )

    # ================= SAVE =================
    if st.button("💾 Save Style"):

        if not style_name.strip():

            st.error("Please Enter Style Name")

            return

        # ================= SIZE LIST =================
        size_list = [

            x.strip()

            for x in sizes.split(",")

            if x.strip()
        ]

        # ================= COLOR LIST =================
        color_list = [

            x.strip()

            for x in colors.split(",")

            if x.strip()
        ]

        ratio_lines = ratio_input.strip().split("\n")

        color_ratios = {}

        try:

            # ================= RATIO LOOP =================
            for line in ratio_lines:

                if "=" not in line:
                    continue

                color, values = line.split("=")

                color = color.strip()

                ratios = [

                    int(x.strip())

                    for x in values.split(",")
                ]

                # ================= VALIDATION =================
                if len(ratios) != len(size_list):

                    st.error(
                        f"{color} ratio count not matching with sizes"
                    )

                    return

                ratio_dict = {}

                for i, size in enumerate(size_list):

                    ratio_dict[size] = ratios[i]

                color_ratios[color] = ratio_dict

            # ================= SAVE STYLE =================
            data[style_name] = {

                "total_qty": int(total_qty),

                # ================= CARTON INFO =================
                "cartons": int(cartons),

                "pcs_per_carton": int(
                    pcs_per_carton
                ),

                # ================= EXTRAS =================
                "extra_percent": float(
                    extra_percent
                ),

                "cut_qty_percent": float(
                    cut_qty_percent
                ),

                # ================= BASIC INFO =================
                "sizes": size_list,

                "colors": color_list,

                "color_ratios": color_ratios
            }

            # ================= SAVE JSON =================
            save_json(FILE, data)

            st.success(
                "✅ Style Saved Successfully"
            )

            st.rerun()

        except Exception as e:

            st.error(f"Error : {e}")

    # ================= DISPLAY =================
    st.markdown("---")

    st.subheader("📂 Saved Styles")

    # ================= EMPTY CHECK =================
    if not data:

        st.info("No styles saved")

        return

    # ================= DISPLAY LOOP =================
    for style, details in data.items():

        st.markdown("---")

        st.write(f"## 🧵 {style}")

        # ================= METRICS =================
        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Order Qty",
                details.get(
                    "total_qty",
                    0
                )
            )

        with col2:

            st.metric(
                "Cartons",
                details.get(
                    "cartons",
                    0
                )
            )

        with col3:

            st.metric(
                "PCS / Carton",
                details.get(
                    "pcs_per_carton",
                    0
                )
            )

        with col4:

            st.metric(
                "Pack Extra %",
                details.get(
                    "extra_percent",
                    0
                )
            )

        # ================= CUT EXTRA =================
        st.info(
            f"Cut Qty % : {details.get('cut_qty_percent', 0)}"
        )

        # ================= RATIO TABLE =================
        rows = []

        color_ratios = details.get(
            "color_ratios",
            {}
        )

        for color, ratios in color_ratios.items():

            row = {"Color": color}

            row.update(ratios)

            rows.append(row)

        if rows:

            ratio_df = pd.DataFrame(rows)

            st.dataframe(
                ratio_df,
                use_container_width=True
            )

        # ================= SUMMARY =================
        total_ratio = 0

        for color, ratios in color_ratios.items():

            total_ratio += sum(
                ratios.values()
            )

        st.success(
            f"Total Ratio : {total_ratio}"
        )

        # ================= DELETE =================
        if st.button(
            f"🗑️ Delete {style}",
            key=f"delete_{style}"
        ):

            if style in data:

                del data[style]

                save_json(FILE, data)

                st.success(
                    f"{style} deleted successfully"
                )

                st.rerun()