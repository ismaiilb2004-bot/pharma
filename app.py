import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image, ImageEnhance

st.set_page_config(
    page_title="المنصة الصيدلانية الذكية",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def preprocess_prescription(pil_image):
    gray_image = pil_image.convert('L')
    enhancer = ImageEnhance.Contrast(gray_image)
    high_contrast = enhancer.enhance(2.5)
    sharp_enhancer = ImageEnhance.Sharpness(high_contrast)
    return sharp_enhancer.enhance(2.0)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    api_key = None

vision_model = genai.GenerativeModel('gemini-2.5-flash') if api_key else None

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("pharmaa.csv")
        df['Nom_Commercial'] = df['Nom_Commercial'].fillna('').astype(str)
        df['DCI'] = df['DCI'].fillna('').astype(str)
        df['Dosage'] = df['Dosage'].fillna('').astype(str)
        df['Prix_DZD'] = pd.to_numeric(df['Prix_DZD'], errors='coerce').fillna(0)
    except:
        df = pd.DataFrame({
            "Nom_Commercial": ["Doliprane"],
            "DCI": ["Paracétamol"],
            "Dosage": ["1000mg"],
            "Prix_DZD": [25.00]
        })
    return df

df = load_data()

# 1. تحميل صورة الخلفية (رابط مباشر لصورة صيدلية عالية الجودة من Unsplash)
import base64
import requests
from io import BytesIO

def load_bg_image():
    url = "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?q=80&w=1920&auto=format&fit=crop"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return base64.b64encode(resp.content).decode()
    except Exception:
        # صورة خلفية احتياطية (تدرج أزرق داكن) إذا فشل تحميل الصورة
        return None

bg_b64 = load_bg_image()

# 2. إضافة تأثير CSS الزجاجي Glassmorphism
if bg_b64:
    bg_style = f"""
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_b64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(15, 23, 42, 0.35);
        backdrop-filter: blur(8px) saturate(120%);
        -webkit-backdrop-filter: blur(8px) saturate(120%);
        z-index: 0;
    }}
    .stApp > div:first-child {{ position: relative; z-index: 1; }}
    """
else:
    bg_style = """
    .stApp {
        background: linear-gradient(135deg, #0b1329 0%, #101f42 100%);
        color: #f1f5f9;
    }
    """

st.markdown(f"""
<style>
    {bg_style}

    .main {{
        direction: rtl;
        text-align: right;
    }}
    
    /* تحويل البطاقات إلى نمط زجاجي شفاف */
    .drug-card, .analysis-card, .top-header {{
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(12px) saturate(140%);
        -webkit-backdrop-filter: blur(12px) saturate(140%);
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }}

    .top-header {{
        background: linear-gradient(90deg, rgba(30, 60, 114, 0.85) 0%, rgba(42, 82, 152, 0.85) 100%) !important;
    }}

    .drug-card {{
        margin-top: 10px;
    }}

    .drug-title {{
        color: #38bdf8;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 5px;
    }}

    .dci-badge {{
        background-color: rgba(15, 23, 42, 0.85);
        color: #34d399;
        padding: 6px 12px;
        border-radius: 6px;
        font-family: monospace;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #059669;
    }}

    .price-box {{
        background-color: rgba(6, 78, 59, 0.85) !important;
        color: #6ee7b7;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        border: 1px solid rgba(110, 231, 183, 0.3);
    }}

    .analysis-card {{
        border-right: 5px solid #10b981;
    }}

    /* جعل جميع النصوص واضحة ومقروءة فوق الزجاج */
    .stMarkdown, .stText, .stHeader, h1, h2, h3, h4, p, label, .stRadio label, .stButton > button {{
        color: #f1f5f9 !important;
    }}

    /* خلفية شفافة للعناصر التفاعلية */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stFileUploader, .stRadio {{
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }}

    .stTextInput label, .stSelectbox label, .stFileUploader label {{
        color: #f1f5f9 !important;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-header">
    <div>
        <h2>💊 المنصة الصيدلانية الذكية</h2>
        <p>نظام إدارة الأدوية والتحليل الآلي للوصفات الطبية بالذكاء الاصطناعي</p>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 البحث اليدوي والتحليل", "📷 قراءة وصفة طبية (Ordonnance)"])

with tab1:
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("مركز البحث السريع")
        search_type = st.radio("البحث بواسطة:", ["الاسم التجاري", "المادة الفعالة (DCI)"], horizontal=True)
        
        if search_type == "الاسم التجاري":
            drug_list = sorted(df["Nom_Commercial"].unique().tolist())
            selected_drug = st.selectbox("اختر أو اكتب اسم الدواء:", drug_list)
            selected_data = df[df["Nom_Commercial"] == selected_drug].iloc[0]
        else:
            dci_list = sorted(df["DCI"].unique().tolist())
            selected_drug = st.selectbox("اختر أو اكتب المادة الفعالة:", dci_list)
            selected_data = df[df["DCI"] == selected_drug].iloc[0]
        
        st.write("")
        ai_btn = st.button("✨ تشغيل التحليل بالذكاء الاصطناعي", use_container_width=True, type="primary")

    with c2:
        st.subheader("تفاصيل الدواء المحدد")
        
        st.markdown(f"""
        <div class="drug-card">
            <div class="drug-title">{selected_data['Nom_Commercial']}</div>
            <div class="dci-badge">🧪 {selected_data['DCI']} | {selected_data['Dosage']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_price, col_status = st.columns([1, 1])
        with col_price:
            st.markdown(f"""
            <div class="price-box">
                <small style="font-size:0.8rem; display:block; color:#a7f3d0;">السعر المعتمد</small>
                {selected_data['Prix_DZD']} د.ج
            </div>
            """, unsafe_allow_html=True)
        
        with col_status:
            st.info("💡 **حالة التعويض:** الدواء قابل للتعويض ضمن شبكة الشفاء (CHIFA).")

        if ai_btn:
            if not vision_model:
                st.error("⚠️ يرجى إعداد مفتاح API في secrets.toml")
            else:
                try:
                    with st.spinner("جاري التحليل..."):
                        prompt = f"حلل دواء {selected_data['Nom_Commercial']} (DCI: {selected_data['DCI']}) في الجزائر: دواعي، بدائل، نصائح."
                        response = vision_model.generate_content(prompt)
                        st.markdown(f'<div class="analysis-card">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"خطأ: {e}")

with tab2:
    st.subheader("قراءة وتحليل الوصفات الطبية بالذكاء الاصطناعي")
    uploaded_file = st.file_uploader("ارفع صورة الوصفة الطبية هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        raw_image = Image.open(uploaded_file)
        processed_image = preprocess_prescription(raw_image)
        
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(raw_image, caption="📷 الصورة الأصلية", use_container_width=True)
        with col_img2:
            st.image(processed_image, caption="⚡ الصورة المعالجة", use_container_width=True)
        
        if st.button("🔍 قراءة وتحليل الوصفة", type="primary", use_container_width=True):
            if not vision_model:
                st.error("⚠️ يرجى إعداد مفتاح API أولاً.")
            else:
                try:
                    with st.spinner("جاري قراءة الخط اليدوي..."):
                        available_drugs = df['Nom_Commercial'].tolist()
                        
                        prompt = f"""
                        أنت مساعد صيدلي خبير في الجزائر. أمامك صورة لوصفة طبية تم تحسينها رقمياً.

                        📜 قائمة الأدوية المتاحة:
                        {available_drugs[:2000]}

                        المطلوب:
                        1. اقرأ الاسم المكتوب بحرفيته دون استبدال.
                        2. طابقه مع القائمة أعلاه.
                        3. اعرض النتائج في جدول:
                        | # | الاسم المكتوب | الدواء المطابق | DCI | الجرعة | الكمية |
                        ثم أضف الملاحظات والتنبيهات.
                        """
                        
                        response = vision_model.generate_content([prompt, processed_image])
                        st.markdown(f'<div class="analysis-card">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
