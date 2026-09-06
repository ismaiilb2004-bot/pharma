@echo off
REM ============================================================
REM  سكربت النشر التلقائي إلى GitHub
REM  يرفع الملفات الآمنة فقط (بدون المفتاح السري!)
REM ============================================================

cd /d "%~dp0"

echo.
echo === خطوة 1: تهيئة Git (اول مرة فقط) ===
git init 2>nul

echo.
echo === خطوة 2: إضافة الملفات الآمنة فقط ===
git add app.py requirements.txt pharmaa.csv README.md .gitignore run.bat

echo.
echo === خطوة 3: التأكد من عدم رفع المفتاح السري ===
git status

echo.
echo === افحص القائمة أعلاه: يجب ألا يكون secrets.toml موجوداً فيها ===
echo.
pause

echo.
echo === خطوة 4: إنشاء أول إصدار ===
git commit -m "منصة الصيدلية الذكية - الإصدار الأول"

echo.
echo === خطوة 5: ربط المخزن البعيد (ضع رابط مخزنك هنا) ===
echo git remote add origin https://github.com/اسم_مستخدمك/pharma.git
echo git branch -M main
echo git push -u origin main

echo.
echo ============================================================
echo  تم التحضير! الآن:
echo  1. أنشئ مخزناً على GitHub باسم pharma
echo  2. عدلت الأوامر أعلاه برابط مخزنك ثم نفذها يدوياً
echo  3. اذهب إلى share.streamlit.io وانشر
echo ============================================================
pause
