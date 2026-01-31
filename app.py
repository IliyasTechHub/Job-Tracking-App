import streamlit as st
import pandas as pd


# Page config

st.set_page_config(page_title="Job Tracker App", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
    }
    </style>
""", unsafe_allow_html=True)



# Title Section (Markdown Styled)

st.markdown(
    """
    <div style='text-align:center; padding:20px;'>
        <h1 style='color:#4B0082; margin-bottom:0;'>🚀 Job Tracking Dashboard</h1>
        <h4 style='color:#555; margin-top:5px;'>Track Applications, Status & Follow-ups</h4>
        <hr style='border:1px solid #ccc; margin-top:10px'>
    </div>
    """,
    unsafe_allow_html=True
)


# Load CSV

df = pd.read_csv("jobsv3.csv")
df1 = df.copy()
df1 = df1.dropna(subset=["Companies Name"])
df1 = df1.drop_duplicates(subset=["Companies Name"])


# Status Metrics (Markdown Cards)

st.subheader("📊 Status Overview")
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div style='background-color:#D6EAF8; padding:20px; border-radius:15px; text-align:center;'>
    <h3>Total Companies</h3>
    <h2 style='color:#2E86C1;'>{df1['Companies Name'].nunique()}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style='background-color:#D5F5E3; padding:20px; border-radius:15px; text-align:center;'>
    <h3>✅ Applied</h3>
    <h2 style='color:#28B463;'>{(df1['Status'] == 'Applied').sum()}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style='background-color:#FCF3CF; padding:20px; border-radius:15px; text-align:center;'>
    <h3>⏳ Pending</h3>
    <h2 style='color:#D68910;'>{(df1['Status'] == 'Pending').sum()}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# Sidebar Filters (Markdown Styled Headers)

st.sidebar.markdown("## 🔍 Filters")
city = st.sidebar.multiselect("Select City", options=df1["City"].dropna().unique())
status = st.sidebar.multiselect("Select Status", options=df1["Status"].dropna().unique())
role = st.sidebar.multiselect("Select Role", options=df1["Roles"].dropna().unique())

filtered_df = df1.copy()
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]
if status:
    filtered_df = filtered_df[filtered_df["Status"].isin(status)]
if role:
    filtered_df = filtered_df[filtered_df["Roles"].isin(role)]

st.subheader("🏢 Data of Companies")
if st.button("Show Companies"):
    st.dataframe(filtered_df, use_container_width=True)




# Follow-up Summary

st.subheader("📋 Follow-up Summary")
followup_cols = ["Follow-up-1(24hrs)", "Follow-up-2(48hrs)", "Follow-up-3(100 HRS)"]
total_followups = df1[followup_cols].count().sum()
done_count = (df1[followup_cols] == "DONE").sum().sum()
pending_count = (df1[followup_cols] == "PENDING").sum().sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Follow-ups", total_followups)
col2.metric("✅ Follow-ups Done", done_count)
col3.metric("⏳ Follow-ups Pending", pending_count)

st.markdown("---")


# Details of companies

company = st.selectbox("Select Company", df1["Companies Name"].unique(), key="company_main")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📨 Mark as Applied", key=f"applied_{company}"):
        df.loc[df["Companies Name"] == company, "Status"] = "Applied"
        df.to_csv("jobsv3.csv", index=False)
        st.success("Applied ✅")

with col2:
    if st.button("✅ Follow-up DONE", key=f"followup_{company}"):
        df.loc[df["Companies Name"] == company, "Follow-up-1(24hrs)"] = "DONE"
        df.to_csv("jobsv3.csv", index=False)
        st.success("Follow-up DONE ✅")

with col3:
    career_link = df1.loc[df1["Companies Name"] == company, "Career Link"].values[0]
    if pd.notna(career_link):
        st.markdown(
            f"<a href='{career_link}' target='_blank'>🚀 Click to Apply</a>",
            unsafe_allow_html=True
        )

st.markdown("---")


# Check Follow-ups

st.subheader("📌 Follow-ups")

if st.checkbox("Click To Check Companies with Pending Follow-ups"):
    Pending_df = df1[
        (df1["Follow-up-1(24hrs)"] == "PENDING") |
        (df1["Follow-up-2(48hrs)"] == "PENDING") |
        (df1["Follow-up-3(100 HRS)"] == "PENDING")
    ]
    st.dataframe(Pending_df, use_container_width=True)

if st.checkbox("Click To Check Companies with Done Follow-ups"):
    Done_df = df1[
        (df1["Follow-up-1(24hrs)"] == "DONE") |
        (df1["Follow-up-2(48hrs)"] == "DONE") |
        (df1["Follow-up-3(100 HRS)"] == "DONE")
    ]
    st.dataframe(Done_df, use_container_width=True)

st.markdown("---")


# Add New Company

if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False

if st.button("➕ Add New Company"):
    st.session_state.show_add_form = not st.session_state.show_add_form

if st.session_state.show_add_form:
    st.subheader("➕ Add New Company")
    with st.form("add_company_form"):
        comp_name = st.text_input("Company Name")
        city = st.text_input("City")
        hr_mail = st.text_input("HR Email")
        career_link = st.text_input("Career Link")
        status = st.selectbox("Status", ["Applied", "Pending", "Rejected"], index=1)
        role = st.text_input("Role")
        package = st.text_input("Package")
        experience = st.text_input("Experience")
        mode = st.selectbox("WFH / WFO", ["WFH", "WFO", "Hybrid"])
        skills = st.text_input("Skills (comma separated)")
        submit = st.form_submit_button("Add Company")

    if submit:
        comp_clean = comp_name.strip()
        if comp_clean == "":
            st.error("❌ Company name is required")
        else:
            existing_companies = df["Companies Name"].dropna().str.strip().str.lower().values
            if comp_clean.lower() in existing_companies:
                st.warning("⚠️ Company already exists")
            else:
                new_row = {
                    "Companies Name": comp_clean,
                    "City": city,
                    "HR Mail ID": hr_mail,
                    "Career Link": career_link,
                    "Status": status,
                    "Roles": role,
                    "Packages": package,
                    "Experience": experience,
                    "WFH/WFO": mode,
                    "Skills": skills,
                    "Follow-up-1(24hrs)": "PENDING",
                    "Follow-up-2(48hrs)": "PENDING",
                    "Follow-up-3(100 HRS)": "PENDING"
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv("jobsv3.csv", index=False)
                st.success("✅ New company added successfully!")
                st.session_state.show_add_form = False
                st.experimental_rerun()


# Background

st.markdown(
    """
    <style>
    .stApp {
        background-color: #b6e9f2;
        color: #000;                 
    }

    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #4B0082;
    }

    
    .metric-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
        color: #000;
    }

    
    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #6A0DAD;
        color: #fff;
    }

  
    .dataframe, .stDataFrame {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <style>
   
    [data-testid="stSidebar"] > div:first-child {{
        background-color: #c0fc77;
    }}
    </style>
    """,
    unsafe_allow_html=True
)





        
















