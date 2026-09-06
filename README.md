# 💊 المنصة الصيدلانية الذكية

نظام إدارة الأدوية والقراءة الآلية للوصفات الطبية بالذكاء الاصطناعي.

## ✨ الميزات

- 🔍 **البحث اليدوي**: بحث سريع في قاعدة بيانات الأدوية الجزائرية (الاسم التجاري أو المادة الفعالة)
- 🤖 **التحليل الذكي**: تحليل الدواء بالذكاء الاصطناعي (دواعي، بدائل، نصائح)
- 📷 **قراءة الوصفات**: رفع صورة وصفة طبية وقراءتها ومطابقتها مع القاعدة الوطنية للأدوية

## 🚀 التشغيل المحلي

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 النشر على Streamlit Community Cloud

1. **إنشاء حساب GitHub** (مجاني): https://github.com

2. **إنشاء مخزن** (Repository) باسم `pharma`

3. **رفع هذه الملفات فقط**:
   - `app.py`
   - `requirements.txt`
   - `pharmaa.csv`
   - `README.md`
   - `.gitignore`
   - `run.bat`

   ⚠️ **لا ترفع أبداً** ملف `.streamlit/secrets.toml` لأنه يحتوي على مفتاح API السري (محمي بـ `.gitignore`).

4. **النشر على Streamlit**:
   - اذهب إلى https://share.streamlit.io
   - سجّل الدخول بـ GitHub
   - اضغط **"Create app"** ← اختر المخزن `pharma` وملف `app.py`
   - اضغط **"Deploy"**

5. **إضافة المفتاح السري**:
   - في لوحة تحكم التطبيق اضغط **"Settings"**
   - اذهب إلى **"Secrets"**
   - أضِف:
     ```toml
     GEMINI_API_KEY = "مفتاحك_السري_هنا"
     ```
   - اضغط **"Save"** ثم **"Rerun"**

## 🔐 الحصول على مفتاح Gemini API

احصل على مفتاح مجاني من: https://aistudio.google.com/app/apikey

## 📁 هيكل المشروع

```
pharma/
├── app.py              # كود التطبيق الرئيسي
├── requirements.txt    # المكتبات المطلوبة
├── pharmaa.csv         # قاعدة البيانات
├── run.bat             # سكربت التشغيل (Windows)
├── .gitignore          # حماية الملفات السرية
├── .streamlit/
│   └── secrets.toml    # مفتاح API (سري - لا يُرفع)
└── clean_data.py       # تنظيف الأدوية (اختياري)
```
