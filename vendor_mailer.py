import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def vendor_mailer_module():

    st.header("AI Vendor Mail Sender")

    # ------------------ COMPANY INFO ------------------
    st.subheader("Your Company Details")

    company_name = st.text_input("Company Name", value="PRP Garments")
    phone = st.text_input("Phone Number", value="7708058574")
    sender_email = st.text_input("Your Email")
    sender_password = st.text_input("Your Email App Password", type="password")

    # ------------------ DEPARTMENT SELECT ------------------
    st.subheader("Select Department")

    department = st.selectbox(
        "Department",
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
            "Washing"
        ]
    )

    # ------------------ REQUIREMENT DETAILS ------------------
    st.subheader("Requirement Details")

    requirement = st.text_area("Enter Your Requirement Details")

    # ------------------ NUMBER OF COMPANIES ------------------
    num_companies = st.number_input(
        "Number of Companies to Send Mail",
        min_value=1,
        max_value=20,
        value=1
    )

    # Dynamic email fields
    email_list = []
    st.subheader("Enter Receiver Email IDs")

    for i in range(int(num_companies)):
        email = st.text_input(f"Email ID {i+1}", key=f"email_{i}")
        if email:
            email_list.append(email)

    # ------------------ GENERATE EMAIL CONTENT ------------------
    def generate_email_content(department):

        if department == "Yarn":
            subject = "Enquiry for Yarn Requirement"
            body = f"""
Dear Sir/Madam,

We are looking for {requirement}.

Kindly share your latest price, availability and payment terms.

Company: {company_name}
Contact: {phone}

Regards,
{company_name}
"""

        elif department == "Dyeing":
            subject = "Fabric Dyeing Requirement Enquiry"
            body = f"""
Dear Sir/Madam,

We require dyeing service for {requirement}.

Please share your dyeing charges per kg and lead time.

Company: {company_name}
Contact: {phone}

Regards,
{company_name}
"""

        elif department == "Knitting":
            subject = "Knitting Requirement Enquiry"
            body = f"""
Dear Sir/Madam,

We require knitting service for {requirement}.

Kindly share your knitting charges per kg.

Company: {company_name}
Contact: {phone}

Regards,
{company_name}
"""

        else:
            subject = f"{department} Service Enquiry"
            body = f"""
Dear Sir/Madam,

We require {department} service for {requirement}.

Kindly share your quotation and terms.

Company: {company_name}
Contact: {phone}

Regards,
{company_name}
"""

        return subject, body

    subject, body = generate_email_content(department)

    st.subheader("Preview Email")
    st.write("Subject:", subject)
    st.text(body)

    # ------------------ SEND MAIL ------------------
    if st.button("Send Emails"):

        if not sender_email or not sender_password:
            st.error("Enter your email and app password")
            return

        if len(email_list) == 0:
            st.error("Enter at least one receiver email")
            return

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)

            for receiver in email_list:

                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = receiver
                msg["Subject"] = subject

                msg.attach(MIMEText(body, "plain"))

                server.sendmail(sender_email, receiver, msg.as_string())

            server.quit()

            st.success("Emails Sent Successfully")

        except Exception as e:
            st.error(f"Error: {e}")
