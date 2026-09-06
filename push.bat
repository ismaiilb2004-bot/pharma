@echo off
REM ============================================================
REM  push.bat — رفع التعديلات إلى GitHub تلقائياً
REM  بضغطة واحدة: يرفع الملفات الآمنة ويحدث موقع Streamlit
REM ============================================================

cd /d "%~dp0"

echo.
echo === رفع التعديلات إلى GitHub ===

REM 1. إضافة الملفات الآمنة فقط (بدون المفتاح السري)
git add app.py requirements.txt pharmaa.csv README.md .gitignore run.bat

REM 2. التحقق من وجود تغييرات
git diff --cached --quiet
if %errorlevel%==0 (
    echo لا توجد تغييرات جديدة.
    goto done
)

REM 3. إنشاء رسالة الالتزام مع التاريخ
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value ^| find "="') do set dt=%%I
set commit_msg=تحديث تلقائي %dt:~0,4%-%dt:~4,2%-%dt:~6,2% %dt:~8,2%:%dt:~10,2%

git commit -m "%commit_msg%"

REM 4. دفع التعديلات إلى GitHub
git push origin main

if %errorlevel%==0 (
    echo.
    echo ============================================================
    echo  تم الرفع بنجاح! Streamlit Cloud سيتحدث تلقائياً خلال دقائق.
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo  فشل الرفع. تأكد من:
    echo   - تثبيت Git ثم العب بالمخزن عبر "git_publish.bat" أولاً
    echo   - الاتصال بالإنترنت
    echo ============================================================
)

:done
pause
