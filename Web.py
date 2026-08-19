import datetime
import streamlit as st  # pyright: ignore[reportMissingImports]

st.set_page_config(
    page_title="Case Management Intake Portal",
    layout="wide"
)

st.sidebar.markdown("**Case Management System**")
st.sidebar.info("Module: **SNAP & Medicaid Screening**")
st.sidebar.caption(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")

st.title("Client Intake & Eligibility Screening Portal")
st.write("Determine preliminary eligibility guidelines, gross income thresholds, and required documentation.")

st.divider()

# Section 1: Household & Income Screening
st.markdown("**1. Income & Household Eligibility Screener**")

col1, col2 = st.columns(2)

with col1:
    household_size = st.number_input("Household Size (Include all dependents):", min_value=1, max_value=10, value=3)
    program_type = st.selectbox("Program Assistance Type:", ["SNAP (Food Stamps)", "Medicaid (Adult)", "Medicaid (Aged, Blind, Disabled)"])

with col2:
    gross_monthly_income = st.number_input("Total Household Gross Monthly Income ($):", min_value=0.0, value=2500.00, step=50.0)
    has_elderly_disabled = st.checkbox("Household includes members 60+ or with verified disability")

# Eligibility Threshold Logic (Simplified Base Guidelines)
snap_base_limit = 1580 + ((household_size - 1) * 560)  # Standard 130% FPL estimation
medicaid_base_limit = 1640 + ((household_size - 1) * 580)

if st.button("Calculate Preliminary Eligibility"):
    st.divider()
    
    if "SNAP" in program_type:
        limit = snap_base_limit * (1.65 if has_elderly_disabled else 1.0)
        st.markdown(f"**Program Standard:** SNAP Gross Income Limit for household size of **{household_size}** is approx **${limit:,.2f}/mo**")
        
        if gross_monthly_income <= limit:
            st.success(f"**PRELIMINARY PASS:** Income of ${gross_monthly_income:,.2f} is under the gross limit.")
        else:
            st.warning(f"**OVER INCOME LIMIT:** Income exceeds ${limit:,.2f}. Check for applicable deductions (shelter, medical, child care).")

    elif "Medicaid" in program_type:
        limit = medicaid_base_limit
        st.markdown(f"**Program Standard:** Estimated Medicaid Threshold for household size of **{household_size}** is approx **${limit:,.2f}/mo**")
        
        if gross_monthly_income <= limit:
            st.success(f"**PRELIMINARY PASS:** Income of ${gross_monthly_income:,.2f} meets baseline criteria.")
        else:
            st.error(f"**POTENTIALLY INELIGIBLE:** Income exceeds estimated baseline standard.")

st.divider()

# Section 2: Verification Checklist Generator
st.markdown("**2. Case Documentation & Verification Checklist**")
st.write("Select verified client circumstances to generate required verification documents for the case file.")

c1, c2, c3 = st.columns(3)
with c1:
    v_earned = st.checkbox("Earned Income (W2 / Pay Stubs)")
    v_unearned = st.checkbox("Unearned Income (SSI, SSDI, Unemployment)")
with c2:
    v_shelter = st.checkbox("Shelter Expenses (Rent / Mortgage)")
    v_utility = st.checkbox("Utility Expenses (Electric, Gas, Water)")
with c3:
    v_medical = st.checkbox("Out-of-Pocket Medical Expenses")
    v_citizenship = st.checkbox("Identity & Citizenship Documents")

if st.button("Generate Required Verification List"):
    required_docs = []
    
    if v_earned:
        required_docs.append("Last 30 days of consecutive pay stubs or employer verification form.")
    if v_unearned:
        required_docs.append("Official award letter or current bank statement showing direct deposit.")
    if v_shelter:
        required_docs.append("Current lease agreement, mortgage statement, or rent receipt.")
    if v_utility:
        required_docs.append("Most recent utility bill showing service address.")
    if v_medical:
        required_docs.append("Itemized medical receipts or pharmacy printouts (for elderly/disabled members).")
    if v_citizenship:
        required_docs.append("State ID/Driver's License and Social Security Card or Birth Certificate.")
        
    if required_docs:
        st.write("**Required Action Items for Client Case File:**")
        for doc in required_docs:
            st.info(f"• {doc}")
    else:
        st.warning("No verification items selected.")