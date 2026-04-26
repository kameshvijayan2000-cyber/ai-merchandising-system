import streamlit as st
import pandas as pd
import os
import json

print("NEW FABRIC PROGRAM LOADED")

DATA_FILE = "data/fabric_styles.json"


# ✅ CASE NORMALIZER
def normalize_text(text):
    if isinstance(text, str):
        return text.strip().title()
    return text


def load_styles():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_styles(data):
    if not os.path.exists("data"):
        os.makedirs("data")

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# 🔥 MAIN FUNCTION
def run():

    st.header("🧵 Fabric Program Calculator")

    styles = load_styles()

    # ✅ NORMALIZE OLD DATA (IMPORTANT)
    normalized_styles = {}
    for k, v in styles.items():
        new_key = normalize_text(k)

        df_temp = pd.DataFrame(v)
        if "Color" in df_temp.columns:
            df_temp["Color"] = df_temp["Color"].apply(normalize_text)

        normalized_styles[new_key] = df_temp.to_dict(orient="records")

    styles = normalized_styles
    save_styles(styles)

    # ---------- SELECT STYLE ----------
    style_list = list(styles.keys())
    selected_style = st.selectbox("Select Saved Style", ["New Style"] + style_list)

    # ================= VIEW SAVED STYLE =================
    if selected_style != "New Style":
        st.success(f"Loaded: {selected_style}")
        df_loaded = pd.DataFrame(styles[selected_style])

        # ✅ Normalize display
        df_loaded["Color"] = df_loaded["Color"].apply(normalize_text)

        st.dataframe(df_loaded, use_container_width=True)

    else:
        # ---------- INPUT ----------
        style_name = st.text_input("Style Name")

        total_qty = st.number_input("Total Qty", value=7200)
        extra_percent = st.number_input("Extra %", value=7.0)

        size_input = st.text_input("Sizes", "XS,S,M,L,XL")
        sizes_list = [s.strip() for s in size_input.split(",") if s.strip()]

        body_weight = st.number_input("Body Weight", value=0.350)
        rib_weight = st.number_input("Rib Weight", value=0.100)
        sj_weight = st.number_input("SJ Weight", value=0.003)

        body_loss = st.number_input("Body Loss %", value=13.0)
        rib_loss = st.number_input("Rib Loss %", value=10.0)
        sj_loss = st.number_input("SJ Loss %", value=0.0)

        num_colors = st.number_input("No of Colors", min_value=1, value=1)

        color_ratios = {}

        for i in range(int(num_colors)):
            # ✅ Normalize color input
            color = normalize_text(st.text_input(f"Color {i+1}", key=f"c{i}"))
            ratios = {}

            for size in sizes_list:
                ratios[size] = st.number_input(size, key=f"{size}{i}", value=1)

            if color:
                color_ratios[color] = ratios

        # ---------- CALCULATE ----------
        if st.button("Generate Fabric"):

            if not style_name:
                st.warning("Enter Style Name")
                return

            # ✅ Normalize style name
            style_name = normalize_text(style_name)

            results = []

            total_ratio_units = sum(
                sum(v.values()) for v in color_ratios.values()
            )

            base_value = total_qty / total_ratio_units

            for color, sizes in color_ratios.items():

                body_total = 0
                rib_total = 0
                sj_total = 0

                for size, ratio in sizes.items():

                    order_qty = ratio * base_value
                    adjusted_qty = order_qty * (1 + extra_percent / 100)

                    body_total += adjusted_qty * body_weight * (1 + body_loss / 100)
                    rib_total += adjusted_qty * rib_weight * (1 + rib_loss / 100)
                    sj_total += adjusted_qty * sj_weight * (1 + sj_loss / 100)

                results.append({
                    "Color": normalize_text(color),
                    "Body Total (Kg)": round(body_total, 2),
                    "Rib Total (Kg)": round(rib_total, 2),
                    "SJ Total (Kg)": round(sj_total, 2)
                })

            df = pd.DataFrame(results)

            st.dataframe(df, use_container_width=True)

            # SAVE STYLE
            styles[style_name] = df.to_dict(orient="records")
            save_styles(styles)

            st.success(f"✅ Saved style: {style_name}")

    # ================= DELETE =================
    st.markdown("---")
    if style_list:
        st.subheader("🗑️ Delete Style")

        del_style = st.selectbox("Select Style to Delete", style_list)

        if st.button("Delete Style"):
            del styles[del_style]
            save_styles(styles)
            st.success("Deleted")
            st.rerun()

    # ================= 🔥 NEW FEATURE =================
    st.markdown("---")
    st.subheader("📦 All Styles Fabric Summary (Purchase View)")

    if styles:

        all_rows = []

        for style, data in styles.items():

            temp_df = pd.DataFrame(data)
            temp_df["Style"] = normalize_text(style)

            temp_df["Color"] = temp_df["Color"].apply(normalize_text)

            temp_df["Body Total (Kg)"] = pd.to_numeric(temp_df["Body Total (Kg)"], errors="coerce").fillna(0)
            temp_df["Rib Total (Kg)"] = pd.to_numeric(temp_df["Rib Total (Kg)"], errors="coerce").fillna(0)
            temp_df["SJ Total (Kg)"] = pd.to_numeric(temp_df["SJ Total (Kg)"], errors="coerce").fillna(0)

            temp_df["Total (Kg)"] = (
                temp_df["Body Total (Kg)"] +
                temp_df["Rib Total (Kg)"] +
                temp_df["SJ Total (Kg)"]
            )

            all_rows.append(temp_df)

        final_df = pd.concat(all_rows, ignore_index=True)

        for style in final_df["Style"].unique():

            st.markdown(f"### 🧵 Style: {style}")

            style_df = final_df[final_df["Style"] == style]

            st.dataframe(
                style_df[["Color", "Body Total (Kg)", "Rib Total (Kg)", "SJ Total (Kg)", "Total (Kg)"]],
                use_container_width=True
            )

        st.markdown("### 📊 Grand Total")

        total_body = final_df["Body Total (Kg)"].sum()
        total_rib = final_df["Rib Total (Kg)"].sum()
        total_sj = final_df["SJ Total (Kg)"].sum()
        grand_total = final_df["Total (Kg)"].sum()

        summary_df = pd.DataFrame([{
            "Body Total (Kg)": round(total_body, 2),
            "Rib Total (Kg)": round(total_rib, 2),
            "SJ Total (Kg)": round(total_sj, 2),
            "Grand Total (Kg)": round(grand_total, 2)
        }])

        st.dataframe(summary_df, use_container_width=True)

    else:
        st.info("No styles saved yet")

    # ================= COLOR MATRIX =================
    st.markdown("---")
    st.subheader("🎨 Color-wise Fabric Requirement (Style Matrix)")

    if styles:

        matrix_data = []
        breakdown_data = {}

        for style, data in styles.items():

            temp_df = pd.DataFrame(data)
            temp_df["Color"] = temp_df["Color"].apply(normalize_text)

            temp_df["Total"] = (
                temp_df["Body Total (Kg)"] +
                temp_df["Rib Total (Kg)"] +
                temp_df["SJ Total (Kg)"]
            )

            for _, row in temp_df.iterrows():

                color = normalize_text(row["Color"])

                matrix_data.append({
                    "Style": normalize_text(style),
                    "Color": color,
                    "Total": row["Total"]
                })

                if color not in breakdown_data:
                    breakdown_data[color] = {"Body": 0, "Rib": 0, "SJ": 0}

                breakdown_data[color]["Body"] += row["Body Total (Kg)"]
                breakdown_data[color]["Rib"] += row["Rib Total (Kg)"]
                breakdown_data[color]["SJ"] += row["SJ Total (Kg)"]

        matrix_df = pd.DataFrame(matrix_data)

        pivot_df = matrix_df.pivot_table(
            index="Color",
            columns="Style",
            values="Total",
            aggfunc="sum",
            fill_value=0
        )

        pivot_df["Grand Total"] = pivot_df.sum(axis=1)

        st.dataframe(pivot_df, use_container_width=True)

        breakdown_list = []

        for color, vals in breakdown_data.items():

            total = vals["Body"] + vals["Rib"] + vals["SJ"]

            breakdown_list.append({
                "Color": color,
                "Body (Kg)": round(vals["Body"], 2),
                "Rib (Kg)": round(vals["Rib"], 2),
                "SJ (Kg)": round(vals["SJ"], 2),
                "Total (Kg)": round(total, 2)
            })

        st.dataframe(pd.DataFrame(breakdown_list), use_container_width=True)

    else:
        st.info("No styles available")
