import streamlit as st
import json
import os
from modules.utils import clear_all_data

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="PRP Garments System",
    layout="wide"
)

# ================= IMPORT MODULES =================
from modules.fabric_program import run as fabric_program_module
from modules.count_calculator import count_calculator_module
from modules.fabric_store import run as fabric_store_module
from modules.production_tracker import run as production_tracker_module
from modules.master_style import run as master_style_module

# ================= FILES =================
STYLE_FILE = "data/style_master.json"
FABRIC_STORE_FILE = "data/fabric_store.json"
PRODUCTION_FILE = "data/production_tracking.json"

# ================= LOAD JSON =================
def load_json(path):

    if os.path.exists(path):

        with open(path, "r") as f:
            return json.load(f)

    return {}

# ================= LOAD DATA =================
style_data = load_json(STYLE_FILE)
fabric_data = load_json(FABRIC_STORE_FILE)
production_data = load_json(PRODUCTION_FILE)

# ================= CALCULATIONS =================
total_styles = len(style_data)

total_order_qty = 0

for style, details in style_data.items():

    total_order_qty += details.get(
        "total_qty",
        0
    )

total_fabric_stock = 0

if "rolls" in fabric_data:

    for roll in fabric_data["rolls"]:

        total_fabric_stock += float(
            roll.get("Kg", 0)
        )

total_entries = 0

if "entries" in production_data:

    total_entries = len(
        production_data["entries"]
    )

# ================= TITLE =================
st.title("🏭 PRP Garments Management System")

st.caption("AI Merchandising Dashboard")

# ================= OVERVIEW =================
st.markdown("## 📊 Live Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Styles",
        total_styles
    )

with col2:

    st.metric(
        "Order Qty",
        total_order_qty
    )

with col3:

    st.metric(
        "Fabric Stock (Kg)",
        round(total_fabric_stock, 2)
    )

with col4:

    st.metric(
        "Production Entries",
        total_entries
    )

# ================= EXTRA INSIGHTS =================
st.markdown("---")

col5, col6 = st.columns(2)

with col5:

    st.subheader("📋 Current System Status")

    if total_styles == 0:

        st.warning(
            "No styles created"
        )

    else:

        st.success(
            f"{total_styles} styles active in system"
        )

    if total_fabric_stock <= 0:

        st.warning(
            "Fabric stock empty"
        )

    else:

        st.success(
            f"{round(total_fabric_stock,2)} Kg fabric available"
        )

with col6:

    st.subheader("🏭 Production Status")

    if total_entries == 0:

        st.warning(
            "No production entries"
        )

    else:

        st.success(
            f"{total_entries} production entries updated"
        )

# ================= GLOBAL CLEAR =================
with st.expander("⚠️ Danger Zone"):

    st.warning(
        "This will permanently delete ALL saved data."
    )

    confirm = st.checkbox(
        "I understand everything will be deleted"
    )

    if st.button("🗑️ CLEAR COMPLETE SYSTEM"):

        if confirm:

            clear_all_data()

            st.success(
                "All data deleted successfully"
            )

            st.rerun()

        else:

            st.error(
                "Please confirm first"
            )

# ================= SIDEBAR =================
st.sidebar.title("📂 Modules")

option = st.sidebar.radio(

    "Select Module",

    [
        "🏠 Home",
        "📋 Style Master",
        "🧵 Fabric Program",
        "📊 Count Calculator",
        "📁 Fabric Store",
        "🏭 Production Tracker"
    ]
)

# ================= HOME =================
if option == "🏠 Home":

    st.header("🏠 Dashboard")

    st.info(
        "Use the sidebar to navigate between modules."
    )

    st.markdown("---")

    st.subheader("📌 Quick Summary")

    quick1, quick2, quick3 = st.columns(3)

    with quick1:

        st.metric(
            "Styles",
            total_styles
        )

    with quick2:

        st.metric(
            "Orders",
            total_order_qty
        )

    with quick3:

        st.metric(
            "Fabric Kg",
            round(total_fabric_stock, 2)
        )

# ================= STYLE MASTER =================
elif option == "📋 Style Master":

    master_style_module()

# ================= FABRIC PROGRAM =================
elif option == "🧵 Fabric Program":

    fabric_program_module()

# ================= COUNT CALCULATOR =================
elif option == "📊 Count Calculator":

    count_calculator_module()

# ================= FABRIC STORE =================
elif option == "📁 Fabric Store":

    fabric_store_module()

# ================= PRODUCTION TRACKER =================
elif option == "🏭 Production Tracker":

    production_tracker_module()

# ================= FOOTER =================
st.markdown("---")

st.caption(
    "Developed by Kamesh | PRP Garments"
)