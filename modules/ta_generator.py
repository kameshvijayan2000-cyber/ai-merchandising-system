elif option == "📅 T&A":

    st.header("📅 Time & Action Calendar")

    import pandas as pd
    import datetime
    from openpyxl import Workbook

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

    # DEBUG
    st.write("✅ T&A Loaded Successfully")
