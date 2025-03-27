import arabic_reshaper
from bidi.algorithm import get_display
from xhtml2pdf import pisa
import io
import streamlit as st
import base64
from datetime import datetime

def create_download_link(pdf_bytes, filename):
    """Generate a download link for the PDF file"""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">تنزيل الملف</a>'
    return href

def generate_pdf(letter_content, recipient, subject):
    """Generate a PDF file from the letter content"""
    # Reshape Arabic text for proper rendering
    reshaped_text = arabic_reshaper.reshape(letter_content)
    bidi_text = get_display(reshaped_text)
    
    # Current date for filename
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"letter_{now}.pdf"
    
    # Create HTML template with proper RTL support
    html = f"""
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: a4 portrait;
                margin: 2cm;
            }}
            body {{
                font-family: 'Tajawal', 'Arial', sans-serif;
                direction: rtl;
                text-align: right;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .letter-body {{
                line-height: 1.5;
                white-space: pre-line;
            }}
            .footer {{
                text-align: center;
                font-size: 10px;
                margin-top: 30px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>{subject}</h2>
            <p>إلى: {recipient}</p>
            <p>التاريخ: {datetime.now().strftime("%d/%m/%Y")}</p>
        </div>
        <div class="letter-body">
            {letter_content}
        </div>
        <div class="footer">
            <p>© {datetime.now().year} شركة نت زيرو</p>
        </div>
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    result_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result_file, encoding='UTF-8')
    
    if pisa_status.err:
        return None
    
    result_file.seek(0)
    return result_file.getvalue(), filename
