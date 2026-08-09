import streamlit as st
import json
import os
from modules.utils import clear_all_data

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Merchandising System",
    page_icon="assets/app_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= IMPORT MODULES =================
from modules.fabric_program import run as fabric_program_module
from modules.count_calculator import count_calculator_module
from modules.fabric_store import run as fabric_store_module
from modules.production_tracker import run as production_tracker_module
from modules.master_style import run as master_style_module
from modules.cost_estimator import run as cost_estimator_module

# ================= FILES =================
STYLE_FILE = "data/style_master.json"
FABRIC_STORE_FILE = "data/fabric_store.json"
PRODUCTION_FILE = "data/production_tracking.json"

# ================= CREATE DATA FOLDER =================
if not os.path.exists("data"):
    os.makedirs("data")

# ================= LOAD JSON =================
def load_json(path):

    if os.path.exists(path):

        try:

            with open(path, "r") as f:

                return json.load(f)

        except:

            return {}

    return {}

# ================= LOAD DATA =================
style_data = load_json(STYLE_FILE)
fabric_data = load_json(FABRIC_STORE_FILE)
production_data = load_json(PRODUCTION_FILE)

# ================= FIX INVALID DATA =================
if not isinstance(style_data, dict):
    style_data = {}

if not isinstance(fabric_data, dict):
    fabric_data = {}

if not isinstance(production_data, dict):
    production_data = {}

# ================= CALCULATIONS =================
total_styles = len(style_data)

total_order_qty = 0

for style, details in style_data.items():

    if isinstance(details, dict):

        total_order_qty += details.get(
            "total_qty",
            0
        )

# ================= FABRIC STOCK =================
total_fabric_stock = 0

if "rolls" in fabric_data:

    for roll in fabric_data["rolls"]:

        total_fabric_stock += float(
            roll.get("Kg", 0)
        )

# ================= PRODUCTION =================
total_entries = 0

if "entries" in production_data:

    total_entries = len(
        production_data["entries"]
    )

# ================= TITLE =================
st.title("🏭 MERCHANDISING CALCULATOR")

st.caption("AI Merchandising Dashboard")

# ================= LIVE OVERVIEW =================
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

# ================= STYLE OVERVIEW =================
st.markdown("---")

st.subheader("📋 Style Overview")

if style_data:

    style_rows = []

    for style, details in style_data.items():

        if not isinstance(details, dict):
            continue

        style_rows.append({

            "Style":
            style,

            "Order Qty":
            details.get(
                "total_qty",
                0
            ),

            "Extra %":
            details.get(
                "extra_percent",
                0
            ),

            "Cut Qty %":
            details.get(
                "cut_qty_percent",
                0
            ),

            "Colors":
            len(
                details.get(
                    "colors",
                    []
                )
            ),

            "Sizes":
            len(
                details.get(
                    "sizes",
                    []
                )
            )
        })

    if style_rows:

        st.dataframe(
            style_rows,
            use_container_width=True
        )

else:

    st.info(
        "No styles created yet"
    )

# ================= FABRIC STOCK SUMMARY =================
st.markdown("---")

st.subheader("🧵 Fabric Stock Summary")

if (
    "rolls" in fabric_data and
    fabric_data["rolls"]
):

    st.dataframe(
        fabric_data["rolls"],
        use_container_width=True
    )

else:

    st.info(
        "No fabric stock available"
    )

# ================= PRODUCTION SUMMARY =================
st.markdown("---")

st.subheader("🏭 Production Summary")

if (
    "entries" in production_data and
    production_data["entries"]
):

    prod_df = production_data[
        "entries"
    ]

    summary_rows = []

    process_list = list(set(

        row.get("Process", "")
        for row in prod_df

    ))

    garment_processes = [

        "Cutting",
        "Stitching",
        "Checking",
        "Ironing",
        "Packing"

    ]

    for process in process_list:

        process_entries = [

            row for row in prod_df

            if row.get("Process") == process
        ]

        # =========================================
        # GARMENT PROCESS SUMMARY
        # =========================================

        if process in garment_processes:

            target_qty = sum(

                row.get("Target Qty", 0)

                for row in process_entries
            )

            completed_qty = sum(

                row.get("Qty", 0)

                for row in process_entries
            )

            balance = (
                target_qty -
                completed_qty
            )

            summary_rows.append({

                "Process":
                process,

                "Target":
                round(target_qty, 2),

                "Completed":
                round(completed_qty, 2),

                "Balance":
                round(balance, 2)
            })

        # =========================================
        # FABRIC PROCESS SUMMARY
        # =========================================

        else:

            input_qty = sum(

                row.get("Qty", 0)

                for row in process_entries

                if row.get("Type") == "Input"
            )

            output_qty = sum(

                row.get("Qty", 0)

                for row in process_entries

                if row.get("Type") == "Output"
            )

            balance = (
                input_qty -
                output_qty
            )

            summary_rows.append({

                "Process":
                process,

                "Input":
                round(input_qty, 2),

                "Output":
                round(output_qty, 2),

                "Balance":
                round(balance, 2)
            })

    st.dataframe(
        summary_rows,
        use_container_width=True
    )

else:

    st.info(
        "No production entries available"
    )

# ================= GLOBAL CLEAR =================
st.markdown("---")

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
        "💰 Cost Estimator",
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

    q1, q2, q3, q4 = st.columns(4)

    with q1:

        st.metric(
            "Styles",
            total_styles
        )

    with q2:

        st.metric(
            "Orders",
            total_order_qty
        )

    with q3:

        st.metric(
            "Fabric Kg",
            round(total_fabric_stock, 2)
        )

    with q4:

        st.metric(
            "Production",
            total_entries
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

# ================= COST ESTIMATOR =================
elif option == "💰 Cost Estimator":

    cost_estimator_module()

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