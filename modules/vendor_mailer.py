import streamlit as st
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from modules.utils import load_json, save_json

FILE = "data/vendor_mailer.json"


def vendor_mailer_module():

    st.header("📧 AI Vendor Mail Sender")

    # ================= LOAD DATA =================
    data = load_json(FILE)

    if not isinstance(data, dict):
        data = {}

    # ================= COMPANY INFO =================
    st.subheader("🏢 Company Details")

    old_company = data.get("company_info", {})

    col1, col2 = st.columns(2)

    with col1:

        company_name = st.text_input(
            "Company Name",
            value=old_company.get(
                "company_name",
                "PRP Garments"
            )
        )

        phone = st.text_input(
            "Phone Number",
            value=old_company.get(
                "phone",
                ""
            )
        )

    with col2:

        sender_email = st.text_input(
            "Your Email",
            value=old_company.get(
                "sender_email",
                ""
            )
        )

        sender_password = st.text_input(
            "Gmail App Password",
            type="password"
        )

    # ================= SAVE COMPANY INFO =================
    data["company_info"] = {

        "company_name": company_name,
        "phone": phone,
        "sender_email": sender_email
    }

    save_json(FILE, data)

    # ================= DEPARTMENT =================
    st.markdown("---")

    st.subheader("🏭 Department")

    department = st.selectbox(

        "Select Department",

        [
            "Yarn",
            "Dyeing",
            "Knitting",
            "Labels",
            "Polybag",
            "Carton Box",
            "Printing",
            "Compacting",
            "Raising",
            "Washing",
            "Embroidery",
            "Checking",
            "Ironing",
            "Packing"
        ]
    )

    # ================= REQUIREMENT =================
    st.markdown("---")

    st.subheader("📝 Requirement Details")

    requirement = st.text_area(
        "Enter Requirement Details",
        height=150
    )

    # ================= RECEIVER EMAILS =================
    st.markdown("---")

    st.subheader("📨 Receiver Email IDs")

    num_companies = st.number_input(
        "Number of Companies",
        min_value=1,
        max_value=50,
        value=1
    )

    email_list = []

    for i in range(int(num_companies)):

        email = st.text_input(
            f"Email ID {i+1}",
            key=f"email_{i}"
        )

        if email.strip():
            email_list.append(email.strip())

    # ================= EMAIL GENERATOR =================
    def generate_email_content():

        # ===== YARN =====
        if department == "Yarn":

            subject = "Enquiry for Yarn Requirement"

            body = f"""
Dear Sir/Madam,

Greetings from {company_name}.

We are looking for below yarn requirement:

{requirement}

Kindly share your latest quotation, stock availability, payment terms and delivery schedule.

Awaiting your valuable response.

Thanks & Regards,
{company_name}
Contact : {phone}
"""

        # ===== DYEING =====
        elif department == "Dyeing":

            subject = "Fabric Dyeing Requirement Enquiry"

            body = f"""
Dear Sir/Madam,

Greetings from {company_name}.

We require fabric dyeing service for below requirement:

{requirement}

Kindly share your dyeing charges per kg, process details and lead time.

Thanks & Regards,
{company_name}
Contact : {phone}
"""

        # ===== KNITTING =====
        elif department == "Knitting":

            subject = "Knitting Requirement Enquiry"

            body = f"""
Dear Sir/Madam,

Greetings from {company_name}.

We require knitting service for below requirement:

{requirement}

Please share your knitting charges per kg and machine details.

Thanks & Regards,
{company_name}
Contact : {phone}
"""

        # ===== PRINTING =====
        elif department == "Printing":

            subject = "Printing Requirement Enquiry"

            body = f"""
Dear Sir/Madam,

Greetings from {company_name}.

We require printing service for below styles:

{requirement}

Kindly share printing charges and sampling lead time.

Thanks & Regards,
{company_name}
Contact : {phone}
"""

        # ===== LABELS =====
        elif department == "Labels":

            subject = "Labels Requirement Enquiry"

            body = f"""
Dear Sir/Madam,

Greetings from {company_name}.

We require labels for below requirement:

{requirement}

Please share quotation and delivery timeline.

Thanks & Regards,
{company_name}
Contact : {phone}
"""

        # ===== DEFAULT =====
        else:

            subject = f"{department} Service Requirement"

            body = f"""
Dear Sir/Madam,

Greetings from {company_name}.

We require {department} service for below requirement:

{requirement}

Kindly share your quotation, payment terms and delivery details.

Thanks & Regards,
{company_name}
Contact : {phone}
"""

        return subject, body

    # ================= PREVIEW =================
    subject, body = generate_email_content()

    st.markdown("---")

    st.subheader("👀 Mail Preview")

    st.info(f"Subject : {subject}")

    st.text_area(
        "Email Content",
        value=body,
        height=300
    )

    # ================= SEND EMAIL =================
    st.markdown("---")

    if st.button("📤 Send Emails"):

        if not sender_email.strip():

            st.error("Please enter sender email")
            return

        if not sender_password.strip():

            st.error("Please enter app password")
            return

        if not requirement.strip():

            st.error("Please enter requirement details")
            return

        if len(email_list) == 0:

            st.error("Please enter at least one receiver email")
            return

        try:

            # ===== SMTP =====
            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            # ===== SEND LOOP =====
            sent_count = 0

            for receiver in email_list:

                msg = MIMEMultipart()

                msg["From"] = sender_email

                msg["To"] = receiver

                msg["Subject"] = subject

                msg.attach(
                    MIMEText(body, "plain")
                )

                server.sendmail(
                    sender_email,
                    receiver,
                    msg.as_string()
                )

                sent_count += 1

            server.quit()

            # ===== SAVE HISTORY =====
            if "history" not in data:
                data["history"] = []

            data["history"].append({

                "Department": department,

                "Requirement": requirement,

                "Total Mails": sent_count,

                "Subject": subject
            })

            save_json(FILE, data)

            st.success(
                f"✅ {sent_count} Emails Sent Successfully"
            )

        except Exception as e:

            st.error(f"Error : {e}")

    # ================= HISTORY =================
    st.markdown("---")

    st.subheader("📂 Mail History")

    history = data.get("history", [])

    if history:

        history_df = pd.DataFrame(history)

        st.dataframe(
            history_df,
            use_container_width=True
        )

    else:

        st.info("No Mail History Found")

    # ================= CLEAR HISTORY =================
    st.markdown("---")

    if st.button("🗑️ Clear Mail History"):

        data["history"] = []

        save_json(FILE, data)

        st.success("Mail History Cleared")

        st.rerun()