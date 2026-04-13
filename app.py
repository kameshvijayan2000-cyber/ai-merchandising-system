import streamlit as st

# ================= LOGIN SYSTEM =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong Username or Password")

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


# ================= PAGE SETTINGS =================
st.set_page_config(
    page_title="PRP Garments System",
    page_icon="🏭",
    layout="wide"
)

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

    total_qty = st.number_input("Total Order Quantity", value=7200)
    extra_percent = st.number_input("Extra Quantity %", value=7.0)

    st.subheader("Size Configuration")
    size_input = st.text_input("Enter Sizes", value="XS,S,M,L,XL")
    sizes_list = [s.strip() for s in size_input.split(",") if s.strip()]

    st.subheader("Piece Weights")
    body_weight = st.number_input("Body Weight", value=0.350)
    rib_weight = st.number_input("Rib Weight", value=0.100)
    sj_weight = st.number_input("SJ Weight", value=0.003)

    st.subheader("Process Loss %")
    body_loss = st.number_input("Body Loss", value=13.0)
    rib_loss = st.number_input("Rib Loss", value=10.0)
    sj_loss = st.number_input("SJ Loss", value=0.0)

    st.subheader("Color Ratio")

    num_colors = st.number_input("No of Colors", min_value=1, value=1)

    color_ratios = {}

    for i in range(int(num_colors)):
        color = st.text_input(f"Color {i+1}", key=f"color{i}")

        ratios = {}
        for size in sizes_list:
            ratios[size] = st.number_input(size, key=f"{size}{i}", value=1)

        if color:
            color_ratios[color] = ratios

    if st.button("Generate Fabric"):
        df = calculate_fabric_program(
            total_qty,
            color_ratios,
            body_weight,
            rib_weight,
            sj_weight,
            extra_percent,
            body_loss,
            rib_loss,
            sj_loss
        )
        st.dataframe(df)


# ================= OTHER MODULES =================
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


# ================= COSTING =================
elif option == "💰 Costing":

    st.header("Garment Costing")

    garment_type = st.selectbox("Garment Type",
                               ["T-Shirt Full Sleeve", "T-Shirt Half Sleeve", "Track Pant"])

    length = st.number_input("Length", value=70.0)
    gsm = st.number_input("GSM", value=180.0)
    extra = st.number_input("Extra Fabric", value=10.0)

    if "T-Shirt" in garment_type:
        chest = st.number_input("Chest", value=50.0)
        sleeve = st.number_input("Sleeve Length", value=60.0)
        sleeve_w = st.number_input("Sleeve Width", value=20.0)

        weight = calculate_piece_weight(garment_type, length, chest, sleeve, sleeve_w, gsm, extra)
    else:
        thigh = st.number_input("Thigh", value=30.0)
        weight = calculate_piece_weight(garment_type, length, thigh, 0, 0, gsm, extra)

    st.success(f"Piece Weight: {weight} g")

    fabric_rate = st.number_input("Fabric Cost per Kg", value=0.0)
    trims = st.number_input("Trims Cost", value=0.0)
    packing = st.number_input("Packing Cost", value=0.0)
    cmt = st.number_input("CMT", value=0.0)

    total = (weight / 1000) * fabric_rate + trims + packing + cmt

    st.success(f"Final Cost: ₹ {round(total,2)}")


# ================= T&A =================
elif option == "📅 T&A":
    st.header("T&A Module (Already Built)")
    st.info("Use your existing T&A code here")


# ================= FOOTER =================
st.markdown("---")
st.caption("Developed by Kamesh | PRP Garments")
