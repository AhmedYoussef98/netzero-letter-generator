import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="سجل الخطابات - نت زيرو",
    page_icon="📋",
    layout="wide",
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #19402D;'>سجل الخطابات</h1>", unsafe_allow_html=True)

# Function to fetch letter history
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def fetch_letter_history():
    try:
        # This is a placeholder - you would connect to your actual API
        # Replace with your actual endpoint when ready
        url = "http://128.140.37.194:5000/get-letters"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not fetch letter history"}
    except Exception as e:
        return {"error": str(e)}

# Sample data structure until API is ready
sample_data = {
    "letters": [
        {
            "id": "LTR-001",
            "date": "2025-03-25",
            "type": "خطاب تعاون",
            "recipient": "الهيئة العامة",
            "subject": "طلب تعاون",
            "status": "تم الإرسال"
        },
        {
            "id": "LTR-002",
            "date": "2025-03-24",
            "type": "خطاب رد",
            "recipient": "شركة نت زيرو",
            "subject": "بخصوص الاجتماع السابق",
            "status": "مسودة"
        }
    ]
}

# Fetch data or use sample data for now
# Uncomment this when your API is ready
# data = fetch_letter_history()
data = sample_data

if "error" in data:
    st.error(f"خطأ في جلب البيانات: {data['error']}")
else:
    # Create a dataframe from the data
    df = pd.DataFrame(data["letters"])
    
    # Add search and filter options
    st.markdown("<h3 style='text-align: right;'>بحث وتصفية</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("بحث", placeholder="اكتب كلمة للبحث...")
    
    with col2:
        filter_type = st.selectbox(
            "نوع الخطاب",
            options=["الكل"] + list(df["type"].unique()),
            index=0
        )
    
    with col3:
        filter_status = st.selectbox(
            "الحالة",
            options=["الكل"] + list(df["status"].unique()),
            index=0
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df["recipient"].str.contains(search_term, case=False, na=False) |
            filtered_df["subject"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if filter_type != "الكل":
        filtered_df = filtered_df[filtered_df["type"] == filter_type]
    
    if filter_status != "الكل":
        filtered_df = filtered_df[filtered_df["status"] == filter_status]
    
    # Display the filtered dataframe
    st.markdown("<h3 style='text-align: right;'>قائمة الخطابات</h3>", unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.info("لا توجد خطابات مطابقة لمعايير البحث")
    else:
        # Rename columns for display
        display_df = filtered_df.rename(columns={
            "id": "الرقم المرجعي",
            "date": "التاريخ",
            "type": "النوع",
            "recipient": "المستلم",
            "subject": "الموضوع",
            "status": "الحالة"
        })
        
        # Reorder columns
        display_df = display_df[["الرقم المرجعي", "التاريخ", "النوع", "المستلم", "الموضوع", "الحالة"]]
        
        # Display the dataframe
        st.dataframe(display_df, use_container_width=True)
