import streamlit as st
import pandas as pd
import requests
import time
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="نظام نت زيرو لإنشاء الخطابات",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with better RTL and form control support
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@200;300;400;500;700;800;900&display=swap');

/* Base setup for RTL */
html {
    direction: rtl;
}

* {
    font-family: 'Tajawal', sans-serif !important;
}

/* Fix for Streamlit containers */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Header styling */
h1, h2, h3, h4, h5, h6 {
    text-align: right !important;
    font-weight: 700 !important;
    color: #19402D !important;
}

/* Card styling */
.card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border-top: 4px solid #67C971;
}

.card-header {
    color: #19402D;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f0f0f0;
    font-weight: 600;
}

/* Form controls styling */
label {
    color: #19402D !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-align: right !important;
    display: block !important;
    margin-bottom: 0.5rem !important;
}

.stSelectbox > div > div > div {
    text-align: right !important;
    direction: rtl !important;
}

/* Fix selectbox text alignment */
.stSelectbox div[data-baseweb="select"] > div {
    text-align: right !important;
    direction: rtl !important;
}

.stSelectbox div[data-baseweb="select"] > div > div {
    justify-content: flex-end !important;
}

.stSelectbox div[data-baseweb="select"] > div > div > div {
    position: relative !important;
    left: auto !important;
    right: 0 !important;
}

/* For text inputs */
.stTextInput > div > div > input {
    text-align: right !important;
    direction: rtl !important;
}

/* For text areas */
.stTextArea > div > div > textarea {
    text-align: right !important;
    direction: rtl !important;
}

/* For radio buttons */
.stRadio > div {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-end !important;
}

.stRadio label {
    margin-left: 15px !important;
    margin-right: 0 !important;
}

/* Form button styling */
.stButton > button {
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.primary-btn {
    background-color: #67C971 !important;
    color: white !important;
}

.secondary-btn {
    background-color: white !important;
    color: #19402D !important;
    border: 1px solid #19402D !important;
}

/* Letter preview styling */
.letter-preview {
    background-color: white;
    border-radius: 10px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    height: 100%;
    min-height: 500px;
    position: relative;
    margin-top: 0;
}

/* Letter table styling */
.letter-table {
    width: 100%;
    border-collapse: collapse;
    direction: rtl;
}

.letter-table th {
    background-color: #f8f9fa;
    color: #19402D;
    text-align: right;
    padding: 12px 16px;
    font-weight: 600;
    border-bottom: 2px solid #eee;
}

.letter-table td {
    padding: 12px 16px;
    text-align: right;
    border-bottom: 1px solid #eee;
}

.letter-table tr:hover {
    background-color: rgba(103, 201, 113, 0.05);
}

/* Status badges */
.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.status-sent {
    background-color: rgba(103, 201, 113, 0.1);
    color: #67C971;
}

.status-draft {
    background-color: rgba(25, 64, 45, 0.1);
    color: #19402D;
}

.status-review {
    background-color: rgba(255, 193, 7, 0.1);
    color: #FFC107;
}

/* Action buttons */
.action-button {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
}

.action-button:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

/* Hide Streamlit elements */
.stDeployButton, #MainMenu, footer {
    visibility: hidden !important;
}

div.block-container {
    padding-top: 2rem;
}

/* Fix for header */
.main-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

/* Navigation buttons */
.nav-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.nav-buttons button {
    background-color: white;
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    color: #19402D;
    cursor: pointer;
    transition: all 0.3s ease;
}

.nav-buttons button.active {
    background-color: #67C971;
    color: white;
    border-color: #67C971;
}

.nav-buttons button:hover:not(.active) {
    background-color: #f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# API Service class
class LetterService:
    def __init__(self, base_url="http://128.140.37.194:5000"):
        self.base_url = base_url
        
    def generate_letter(self, category, title, recipient, is_firstTime, prompt):
        url = f"{self.base_url}/generate-letter"
        
        payload = {
            "category": category,
            "title": title,
            "recipient": recipient,
            "is_firstTime": is_firstTime,
            "prompt": prompt
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"فشل إنشاء الخطاب: {response.text}"}
        except Exception as e:
            return {"error": f"حدث خطأ أثناء الاتصال بالخادم: {str(e)}"}
    
    def save_letter(self, letter, letter_type, recipient, subject, is_first_comm):
        url = f"{self.base_url}/save-letter"
        
        payload = {
            "letter": letter,
            "letter_type": letter_type,
            "recipient": recipient,
            "subject": subject,
            "is_first_comm": is_first_comm
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"فشل حفظ الخطاب: {response.text}"}
        except Exception as e:
            return {"error": f"حدث خطأ أثناء الاتصال بالخادم: {str(e)}"}

# Initialize the letter service
letter_service = LetterService()

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'create'
if 'letter_history' not in st.session_state:
    st.session_state.letter_history = []
if 'generated_letter' not in st.session_state:
    st.session_state.generated_letter = None

# Helper functions
def format_date_arabic(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    arabic_months = {
        1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
        7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
    }
    return f"{date_obj.day} {arabic_months[date_obj.month]} {date_obj.year}"

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Header and Navigation
logo_col, title_col = st.columns([1, 6])

try:
    with logo_col:
        st.image("assets/images/netzero_logo.png", width=100)
    with title_col:
        st.markdown("<h1 style='text-align: right; margin-top: 1.5rem;'>نظام إنشاء وإدارة الخطابات</h1>", unsafe_allow_html=True)
except:
    st.markdown("<h1 style='text-align: center;'>نظام نت زيرو لإنشاء الخطابات</h1>", unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 5])

with col1:
    create_btn_class = "active" if st.session_state.page == "create" else ""
    if st.button("إنشاء خطاب", key="nav_create", use_container_width=True):
        set_page("create")

with col2:
    history_btn_class = "active" if st.session_state.page == "history" else ""
    if st.button("سجل الخطابات", key="nav_history", use_container_width=True):
        set_page("history")

st.markdown("<hr style='margin: 1rem 0 2rem 0;'>", unsafe_allow_html=True)

# Page content
if st.session_state.page == "create":
    # Create Letter Page
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-header'>بيانات الخطاب</h3>", unsafe_allow_html=True)
        
        with st.form(key="letter_form"):
            # Explicit options for dropdown to ensure proper display
            letter_types = ["خطاب جديد", "خطاب رد", "خطاب متابعة", "خطاب تعاون"]
            letter_type = st.selectbox(
                "نوع الخطاب",
                options=letter_types,
                index=0,
                format_func=lambda x: x  # Ensure text is displayed as-is
            )
            
            category = "collaboration" if letter_type == "خطاب تعاون" else "general"
            
            recipient = st.text_input(
                "المرسل إليه", 
                placeholder="الجهة أو الشخص"
            )
            
            subject = st.text_input(
                "عنوان الخطاب", 
                placeholder="أدخل عنوان الخطاب"
            )
            
            is_first_comm = st.radio(
                "هل هذه أول مراسلة؟",
                options=["نعم", "لا"],
                horizontal=True,
                index=0
            )
            is_firstTime = "True" if is_first_comm == "نعم" else "False"
            
            prompt = st.text_area(
                "محتوى الخطاب",
                placeholder="اكتب وصفاً تفصيلياً لمحتوى الخطاب",
                height=150
            )
            
            submit_col1, submit_col2 = st.columns(2)
            
            with submit_col1:
                submit_button = st.form_submit_button(
                    label="إنشاء الخطاب",
                    use_container_width=True
                )
                st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #67C971 !important;
                    color: white !important;
                }
                </style>
                """, unsafe_allow_html=True)
            
            with submit_col2:
                clear_button = st.form_submit_button(
                    label="إعادة تعيين",
                    use_container_width=True
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit_button:
            if not recipient or not subject or not prompt:
                st.error("يرجى ملء جميع الحقول المطلوبة")
            else:
                with st.spinner("جاري إنشاء الخطاب..."):
                    result = letter_service.generate_letter(
                        category=category,
                        title=subject,
                        recipient=recipient,
                        is_firstTime=is_firstTime,
                        prompt=prompt
                    )
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.session_state.generated_letter = result["letter"]
                        st.session_state.letter_type = letter_type
                        st.session_state.recipient = recipient
                        st.session_state.subject = subject
                        st.session_state.is_firstTime = is_firstTime
                        st.success("تم إنشاء الخطاب بنجاح!")
                        st.rerun()
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='card-header'>معاينة الخطاب</h3>", unsafe_allow_html=True)
        
        if st.session_state.get("generated_letter"):
            st.markdown("<div class='letter-preview'>", unsafe_allow_html=True)
            
            # Letter metadata
            letter_date = datetime.now().strftime("%Y-%m-%d")
            formatted_date = format_date_arabic(letter_date)
            letter_id = f"LTR-{datetime.now().strftime('%y%m%d')}-{datetime.now().strftime('%H%M%S')}"
            
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; margin-bottom: 1.5rem;'>
                <div style='text-align: left;'>
                    <div style='font-weight: 600; color: #19402D;'>{formatted_date}</div>
                    <div style='color: #666; font-size: 0.8rem;'>{letter_id}</div>
                </div>
                <div style='text-align: right;'>
                    <div style='font-weight: 600; color: #19402D;'>شركة نت زيرو</div>
                    <div style='color: #666; font-size: 0.8rem;'>الرياض، المملكة العربية السعودية</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Subject line
            if hasattr(st.session_state, 'subject'):
                st.markdown(f"<div style='text-align: center; font-weight: 600; margin-bottom: 1.5rem; color: #19402D;'>الموضوع: {st.session_state.subject}</div>", unsafe_allow_html=True)
            
            # Letter content
            edited_letter = st.text_area(
                "تعديل الخطاب",
                value=st.session_state.generated_letter,
                height=350,
                key="letter_editor",
                label_visibility="collapsed"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("حفظ الخطاب", key="save_btn", use_container_width=True):
                    with st.spinner("جاري حفظ الخطاب..."):
                        save_result = letter_service.save_letter(
                            letter=edited_letter,
                            letter_type=st.session_state.letter_type,
                            recipient=st.session_state.recipient,
                            subject=st.session_state.subject,
                            is_first_comm=st.session_state.is_firstTime
                        )
                        
                        if "error" in save_result:
                            st.error(save_result["error"])
                        else:
                            st.success("تم حفظ الخطاب بنجاح!")
                            if "result" in save_result:
                                st.info(f"رقم السطر: {save_result['result']['row_number']}")
            
            with col2:
                if st.button("تنزيل PDF", key="download_btn", use_container_width=True):
                    st.download_button(
                        label="تأكيد التنزيل",
                        data=edited_letter.encode('utf-8'),
                        file_name=f"letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="confirm_download",
                    )
            
            with col3:
                if st.button("حذف", key="clear_btn", use_container_width=True):
                    if "generated_letter" in st.session_state:
                        del st.session_state["generated_letter"]
                    st.rerun()
        else:
            st.markdown("""
            <div class='letter-preview' style='display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                <div style='margin-bottom: 1rem; opacity: 0.4;'>
                    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 4H4C2.9 4 2 4.9 2 6V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4ZM20 18H4V6H20V18ZM6 9V11H10V15H12V11H16V9H12V5H10V9H6Z" fill="#67C971"/>
                    </svg>
                </div>
                <p style='text-align: center; color: #666; font-weight: 500; font-size: 1.1rem;'>لم يتم إنشاء أي خطاب بعد</p>
                <p style='text-align: center; color: #888; font-size: 0.9rem;'>املأ النموذج واضغط على زر "إنشاء الخطاب" لإنشاء خطاب جديد</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "history":
    # Letter History Page
    st.markdown("<h2>سجل الخطابات</h2>", unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("بحث", placeholder="اكتب كلمة للبحث...")
    
    with col2:
        letter_types = ["الكل", "خطاب جديد", "خطاب رد", "خطاب متابعة", "خطاب تعاون"]
        filter_type = st.selectbox(
            "نوع الخطاب",
            options=letter_types,
            index=0,
            format_func=lambda x: x  # Ensure text is displayed as-is
        )
    
    with col3:
        statuses = ["الكل", "تم الإرسال", "مسودة", "قيد المراجعة"]
        filter_status = st.selectbox(
            "الحالة",
            options=statuses,
            index=0,
            format_func=lambda x: x  # Ensure text is displayed as-is
        )
    
    # Sample data for demonstration
    letters = [
        {
            "id": "LTR-250325-001",
            "date": "2025-03-25",
            "type": "خطاب تعاون",
            "recipient": "الهيئة العامة",
            "subject": "طلب تعاون",
            "status": "تم الإرسال"
        },
        {
            "id": "LTR-240325-002",
            "date": "2025-03-24",
            "type": "خطاب رد",
            "recipient": "شركة نت زيرو",
            "subject": "بخصوص الاجتماع السابق",
            "status": "مسودة"
        },
        {
            "id": "LTR-230325-003",
            "date": "2025-03-23",
            "type": "خطاب جديد",
            "recipient": "وزارة البيئة",
            "subject": "مشروع الطاقة المتجددة",
            "status": "تم الإرسال"
        },
        {
            "id": "LTR-220325-004",
            "date": "2025-03-22",
            "type": "خطاب متابعة",
            "recipient": "شركة الاستثمارات المستدامة",
            "subject": "متابعة المشروع المشترك",
            "status": "قيد المراجعة"
        },
        {
            "id": "LTR-210325-005",
            "date": "2025-03-21",
            "type": "خطاب تعاون",
            "recipient": "جامعة الملك سعود",
            "subject": "برنامج التدريب التعاوني",
            "status": "تم الإرسال"
        }
    ]
    
    # Apply filters
    filtered_letters = letters
    
    if search_term:
        filtered_letters = [
            letter for letter in filtered_letters
            if (search_term.lower() in letter["recipient"].lower() or
                search_term.lower() in letter["subject"].lower() or
                search_term.lower() in letter["id"].lower())
        ]
    
    if filter_type != "الكل":
        filtered_letters = [
            letter for letter in filtered_letters
            if letter["type"] == filter_type
        ]
    
    if filter_status != "الكل":
        filtered_letters = [
            letter for letter in filtered_letters
            if letter["status"] == filter_status
        ]
    
    # Display the letters in a table
    if not filtered_letters:
        st.info("لا توجد خطابات مطابقة لمعايير البحث")
    else:
        # Create a proper data table using Streamlit
        letter_data = []
        for letter in filtered_letters:
            # Format date
            formatted_date = format_date_arabic(letter["date"])
            
            # Format status with the appropriate style
            status_class = ""
            if letter["status"] == "تم الإرسال":
                status_class = "status-sent"
            elif letter["status"] == "مسودة":
                status_class = "status-draft"
            elif letter["status"] == "قيد المراجعة":
                status_class = "status-review"
            
            status_html = f'<span class="status-badge {status_class}">{letter["status"]}</span>'
            
            # Format actions
            actions_html = """
            <div style="display: flex; gap: 8px; justify-content: center;">
                <button title="تحميل PDF">📥</button>
                <button title="طباعة">🖨️</button>
                <button title="حذف">🗑️</button>
            </div>
            """
            
            letter_data.append({
                "الرقم المرجعي": letter["id"],
                "التاريخ": formatted_date,
                "النوع": letter["type"],
                "المستلم": letter["recipient"],
                "الموضوع": letter["subject"],
                "الحالة": status_html,
                "الإجراءات": actions_html
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(letter_data)
        
        # Custom styling for the dataframe
        st.markdown("""
        <style>
        .dataframe {
            width: 100%;
            direction: rtl;
            text-align: right;
        }
        .dataframe th {
            text-align: right !important;
            background-color: #f8f9fa;
            color: #19402D;
            font-weight: 600;
            padding: 12px 16px !important;
        }
        .dataframe td {
            text-align: right !important;
            padding: 12px 16px !important;
        }
        .dataframe tr:hover {
            background-color: rgba(103, 201, 113, 0.05);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display the table
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1rem 0; border-top: 1px solid #eee;">
    <img src="assets/images/netzero_logo.png" alt="شعار نت زيرو" width="80" style="margin-bottom: 0.5rem;">
    <p style="color: #19402D; font-weight: 500;">نظام نت زيرو لإنشاء وإدارة الخطابات</p>
    <p style="color: #666; font-size: 0.8rem;">© 2025 جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
