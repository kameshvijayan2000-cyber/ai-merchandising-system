import streamlit as st
import requests
import pandas as pd

def auto_directory_module():

    st.header("AI Auto Directory System – Tiruppur (Live AI Powered)")

    api_key = st.text_input("Enter SerpAPI Key", type="password")

    # ================= CATEGORY SECTION =================
    st.subheader("Select Process Category")

    category_option = st.selectbox(
        "Choose Category",
        ["Yarn Mills", "Labels", "Polybags", "Carton Box",
         "Printing", "Dyeing", "Compacting", "Raising",
         "Washing", "Manual Entry"]
    )

    if category_option == "Manual Entry":
        category = st.text_input("Enter Custom Process Name")
    else:
        category = category_option

    # Yarn count only for yarn
    yarn_count = ""
    if category == "Yarn Mills":
        yarn_count = st.text_input("Enter Yarn Count (Example: 24s)")

    # ================= REQUIREMENT SECTION =================
    st.subheader("Your Requirement (For Checking Purpose Only)")

    quantity = st.number_input("Enter Required Quantity", value=1000.0)

    unit = st.selectbox("Select Unit", ["Kg", "Pcs"])

    qty_text = f"{quantity} {unit}"

    # ================= GENERATE BUTTON =================
    if st.button("Generate AI Directory"):

        if not api_key:
            st.error("Please enter SerpAPI Key")
            return

        if not category:
            st.error("Please enter/select category")
            return

        # =====================================================
        # 1️⃣ GENERAL TOP 20 LIST (NOT BASED ON REQUIREMENT)
        # =====================================================

        st.subheader("Top 20 Tiruppur Companies (General List)")

        general_query = f"Top {category} manufacturers in Tiruppur with email id and contact number"

        general_suppliers = []

        for start in [0, 10]:
            params = {
                "engine": "google",
                "q": general_query,
                "api_key": api_key,
                "num": 10,
                "start": start
            }

            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()

            if "organic_results" in data:
                for result in data["organic_results"]:
                    general_suppliers.append([
                        result.get("title", "NA"),
                        result.get("link", "NA"),
                        result.get("snippet", "NA")
                    ])

        # Remove duplicates
        unique_general = []
        seen = set()

        for g in general_suppliers:
            if g[1] not in seen:
                unique_general.append(g)
                seen.add(g[1])

        general_final = unique_general[:20]

        df_general = pd.DataFrame(
            general_final,
            columns=["Company Name", "Website", "Details"]
        )

        st.success(f"{len(df_general)} Companies Found (General Top List)")
        st.dataframe(df_general)

        # =====================================================
        # 2️⃣ REQUIREMENT BASED SEARCH (FOR YOUR CHECKING)
        # =====================================================

        st.subheader("Requirement Based AI Search (For Verification)")

        if category == "Yarn Mills" and yarn_count:
            req_query = f"{yarn_count} cotton yarn suppliers in Tiruppur for bulk order with contact email"
        else:
            req_query = f"{category} suppliers in Tiruppur for bulk requirement with contact email"

        req_suppliers = []

        for start in [0, 10]:
            params = {
                "engine": "google",
                "q": req_query,
                "api_key": api_key,
                "num": 10,
                "start": start
            }

            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()

            if "organic_results" in data:
                for result in data["organic_results"]:
                    req_suppliers.append([
                        result.get("title", "NA"),
                        result.get("link", "NA"),
                        result.get("snippet", "NA")
                    ])

        unique_req = []
        seen_req = set()

        for r in req_suppliers:
            if r[1] not in seen_req:
                unique_req.append(r)
                seen_req.add(r[1])

        req_final = unique_req[:20]

        df_req = pd.DataFrame(
            req_final,
            columns=["Company Name", "Website", "Details"]
        )

        st.success(f"{len(df_req)} Companies Found (Requirement Based)")
        st.dataframe(df_req)

        # =====================================================
        # DOWNLOAD OPTION
        # =====================================================

        file_name = "tiruppur_ai_directory.xlsx"

        with pd.ExcelWriter(file_name) as writer:
            df_general.to_excel(writer, sheet_name="Top 20 General", index=False)
            df_req.to_excel(writer, sheet_name="Requirement Based", index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "Download Complete Directory Excel",
                f,
                file_name=file_name
            )

        # =====================================================
        # EMAIL TEMPLATE
        # =====================================================

        st.subheader("Business Email Template")

        email_text = f"""
Subject: Business Enquiry – {category} Requirement – Tiruppur

Dear Sir/Madam,

Greetings from PRP Garments, Tiruppur.

We are currently sourcing {category} for our upcoming production.

Requirement Details:
--------------------------------
Category : {category}
"""

        if category == "Yarn Mills" and yarn_count:
            email_text += f"Yarn Count : {yarn_count}\n"

        email_text += f"""Quantity : {qty_text}

Kindly share the following details:
• Latest Price
• MOQ
• Available Stock
• Lead Time
• Payment Terms

Looking forward to your response.

Best Regards,
Kamesh Vijayan
PRP Garments – Tiruppur
Phone: 7708058574
Email: kameshvijayan2000@gmail.com
"""

        st.text_area("Copy & Send This Email", email_text, height=350)
