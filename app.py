import streamlit as st

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()


# ================= IMPORT MODULES =================
from modules.fabric_program import calculate_fabric_program
from modules.piece_weight import calculate_piece_weight
from modules.auto_directory import auto_directory_module
from modules.vendor_mailer import vendor_mailer_module
from modules.count_calculator import count_calculator_module
from modules.fabric_store import run as fabric_store_module
from modules.cutting import run as cutting_module
from modules.planning import run as planning_module
from modules.production_tracker import run as production_tracker_module
from modules.fabric_tracking_advanced import run as fabric_tracking_advanced_module



# ================= PAGE =================
st.set_page_config(page_title="PRP Garments System", layout="wide")

st.title("🏭 PRP Garments Management System")
st.caption("AI Merchandising Dashboard")


# ================= SIDEBAR =================
st.sidebar.title("📂 Modules")

option = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home",
        "🧵 Fabric Program",
        "📊 Count Calculator",
        "📁 Fabric Store",
        "✂️ Cutting",
        "📈 Planning",
        "📧 Vendor Mail",
        "🤖 AI Directory",
        "💰 Costing",
        "📧 Production Tracker",
        "📊 Fabric Tracking Advanced",
        "📅 T&A"
    ]
)

# ================= HOME =================
if option == "🏠 Home":
    st.header("Welcome to PRP Garments System")

    col1, col2, col3 = st.columns(3)

    col1.metric("Orders Running", "12")
    col2.metric("Production Status", "On Track")
    col3.metric("Efficiency", "92%")

    st.info("Use the sidebar to navigate modules")


# ================= FABRIC PROGRAM =================
elif option == "🧵 Fabric Program":

    st.header("Fabric Program Calculator")

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
        color = st.text_input(f"Color {i+1}", key=f"c{i}")
        ratios = {}

        for size in sizes_list:
            ratios[size] = st.number_input(size, key=f"{size}{i}", value=1)

        if color:
            color_ratios[color] = ratios

    if st.button("Generate Fabric"):
        df = calculate_fabric_program(
            total_qty, color_ratios,
            body_weight, rib_weight, sj_weight,
            extra_percent,
            body_loss, rib_loss, sj_loss
        )
        st.dataframe(df)


# ================= MODULE CALLS =================
elif option == "📊 Count Calculator":
    count_calculator_module()

elif option == "📁 Fabric Store":
    fabric_store_module()

elif option == "✂️ Cutting":
    cutting_module()

elif option == "📈 Planning":
    planning_module()

elif option == "📧 Vendor Mail":
    vendor_mailer_module()

elif option == "🤖 AI Directory":
    auto_directory_module()
# ================= Production Tracking =================
elif option == "📧 Production Tracker":
    production_tracker_module()

elif option == "📊 Fabric Tracking Advanced":
    fabric_tracking_advanced_module()

# ================= COSTING =================
elif option == "💰 Costing":

    st.header("Garment Costing Module")

    # -------- PIECE WEIGHT --------
    st.subheader("Piece Weight")

    garment_type = st.selectbox(
        "Garment Type",
        ["T-Shirt Full Sleeve", "T-Shirt Half Sleeve", "Track Pant"]
    )

    length = st.number_input("Length (cm)", value=70.0)
    gsm = st.number_input("GSM", value=180.0)
    extra = st.number_input("Extra Fabric (g)", value=10.0)

    if "T-Shirt" in garment_type:
        chest = st.number_input("Chest", value=50.0)
        sleeve = st.number_input("Sleeve Length", value=60.0)
        sleeve_w = st.number_input("Sleeve Width", value=20.0)

        piece_weight = calculate_piece_weight(
            garment_type, length, chest, sleeve, sleeve_w, gsm, extra
        )
    else:
        thigh = st.number_input("Thigh", value=30.0)
        piece_weight = calculate_piece_weight(
            garment_type, length, thigh, 0, 0, gsm, extra
        )

    st.success(f"Piece Weight: {piece_weight} g")

    piece_weight_kg = piece_weight / 1000

    # -------- FABRIC COST --------
    st.subheader("Fabric Process Cost (Per Kg)")

    process_items = {
        "Yarn": st.number_input("Yarn Rate", value=0.0),
        "Knitting": st.number_input("Knitting Rate", value=0.0),
        "Dyeing": st.number_input("Dyeing Rate", value=0.0),
        "Compacting": st.number_input("Compacting Rate", value=0.0),
        "Raising": st.number_input("Raising Rate", value=0.0),
        "Washing": st.number_input("Washing Rate", value=0.0),
        "Printing": st.number_input("Printing Rate", value=0.0)
    }

    total_fabric_rate = sum(process_items.values())
    fabric_cost = piece_weight_kg * total_fabric_rate

    st.info(f"Fabric Cost / Piece: ₹ {round(fabric_cost,2)}")

    # -------- TRIMS --------
    st.subheader("Trims")

    trim_items = {
        "Main Label": st.number_input("Main Label", 0.0),
        "Wash Care": st.number_input("Wash Care", 0.0),
        "Tag": st.number_input("Tag", 0.0),
        "Thread": st.number_input("Thread", 0.0),
        "Zipper": st.number_input("Zipper", 0.0)
    }

    trim_total = sum(trim_items.values())
    st.info(f"Trim Cost: ₹ {round(trim_total,2)}")

    # -------- PACKING --------
    st.subheader("Packing")

    packing_items = {
        "Hanger": st.number_input("Hanger", 0.0),
        "Polybag": st.number_input("Polybag", 0.0),
        "Carton": st.number_input("Carton", 0.0)
    }

    packing_total = sum(packing_items.values())
    st.info(f"Packing Cost: ₹ {round(packing_total,2)}")

    # -------- FINAL --------
    st.subheader("Final Cost")

    cmt = st.number_input("CMT", value=0.0)

    prime = fabric_cost + trim_total + packing_total + cmt

    overhead = st.number_input("Overhead %", value=12.0)
    margin = st.number_input("Profit %", value=20.0)

    final = prime * (1 + overhead/100) * (1 + margin/100)

    st.success(f"Final Price: ₹ {round(final,2)}")


# ================= T&A =================
elif option == "📅 T&A":

    st.header("📅 Time & Action Calendar")

    import pandas as pd
    import datetime

    # -------- BASIC INFO --------
    style_name = st.text_input("Style Name")
    total_qty = st.number_input("Total Order Quantity", value=5000)
    dispatch_date = st.date_input("Dispatch Date")

    st.subheader("Activity Duration (Days)")

    activities = [
        "Order Receipt",
        "Consumption",
        "BOM",
        "PO Issue",
        "Size Set",
        "PP Meeting",
        "Fabric Inhouse",
        "Cutting",
        "Stitching",
        "Finishing",
        "Packing",
        "Inspection",
        "Dispatch"
    ]

    lead_time = {}

    for act in activities:
        lead_time[act] = st.number_input(act, value=2, key=act)

    # -------- GENERATE --------
    if st.button("Generate T&A"):

        if not style_name:
            st.warning("Enter Style Name")
            st.stop()

        schedule = []
        current_end = dispatch_date

        for act in reversed(activities):
            duration = lead_time[act]
            end = current_end
            start = end - datetime.timedelta(days=duration)

            schedule.append([act, start, end, duration])
            current_end = start

        schedule.reverse()

        df = pd.DataFrame(schedule, columns=[
            "Activity", "Start", "End", "Days"
        ])

        st.subheader("📊 T&A Table")
        st.dataframe(df, use_container_width=True)

        # -------- DOWNLOAD --------
        file_name = f"TNA_{style_name}.xlsx"
        df.to_excel(file_name, index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Download Excel",
                f,
                file_name=file_name
            )



# ================= FOOTER =================
st.markdown("---")
st.caption("Developed by Kamesh | PRP Garments")
