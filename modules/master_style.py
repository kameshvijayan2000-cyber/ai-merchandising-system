import streamlit as st
import pandas as pd
from modules.utils import load_json, save_json

FILE = "data/style_master.json"


def run():

    st.header("📋 Style Master Entry")

    data = load_json(FILE)

    # ================= INPUTS =================
    style_name = st.text_input("Style Name")

    total_qty = st.number_input(
        "Total Qty",
        min_value=1,
        value=1000
    )

    # 🔥 PACKAGE EXTRA %
    extra_percent = st.number_input(
        "Extra Qty % (For Count Calculator / Packing)",
        value=5.0
    )

    # 🔥 CUTTING EXTRA %
    cut_qty_percent = st.number_input(
        "Cut Qty % (For Fabric Program)",
        value=3.0
    )

    sizes = st.text_input(
        "Sizes",
        value="S,M,L,XL"
    )

    colors = st.text_input(
        "Colors",
        value="BLACK,WHITE"
    )

    ratio_input = st.text_area(
        "Enter Ratios\nExample:\nBLACK=1,2,2,1\nWHITE=1,1,1,1"
    )

    # ================= SAVE =================
    if st.button("💾 Save Style"):

        if not style_name:

            st.error("Enter Style Name")
            return

        size_list = [
            x.strip()
            for x in sizes.split(",")
            if x.strip()
        ]

        color_list = [
            x.strip()
            for x in colors.split(",")
            if x.strip()
        ]

        ratio_lines = ratio_input.strip().split("\n")

        color_ratios = {}

        try:

            for line in ratio_lines:

                if "=" not in line:
                    continue

                color, values = line.split("=")

                ratios = [
                    int(x.strip())
                    for x in values.split(",")
                ]

                # ✅ Ratio validation
                if len(ratios) != len(size_list):

                    st.error(
                        f"{color.strip()} ratio count not matching sizes"
                    )
                    return

                ratio_dict = {}

                for i, s in enumerate(size_list):

                    ratio_dict[s] = ratios[i]

                color_ratios[color.strip()] = ratio_dict

            # ================= SAVE DATA =================
            data[style_name] = {

                "total_qty": total_qty,

                # 🔥 For Count Calculator
                "extra_percent": extra_percent,

                # 🔥 For Fabric Program
                "cut_qty_percent": cut_qty_percent,

                "sizes": size_list,

                "colors": color_list,

                "color_ratios": color_ratios
            }

            save_json(FILE, data)

            st.success("✅ Style Saved Successfully")

        except Exception as e:

            st.error(f"Error : {e}")

    # ================= DISPLAY =================
    st.markdown("---")

    st.subheader("📂 Saved Styles")

    if data:

        for style, details in data.items():

            st.write(f"## 🧵 {style}")

            col1, col2, col3 = st.columns(3)

            col1.info(
                f"Order Qty : {details['total_qty']}"
            )

            col2.info(
                f"Pack Extra % : {details.get('extra_percent', 0)}"
            )

            col3.info(
                f"Cut Qty % : {details.get('cut_qty_percent', 0)}"
            )

            rows = []

            for color, ratios in details[
                "color_ratios"
            ].items():

                row = {"Color": color}

                row.update(ratios)

                rows.append(row)

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True
            )

            # ================= DELETE =================
            if st.button(
                f"🗑️ Delete {style}",
                key=style
            ):

                del data[style]

                save_json(FILE, data)

                st.warning(f"{style} deleted")

                st.rerun()

    else:

        st.info("No styles saved")