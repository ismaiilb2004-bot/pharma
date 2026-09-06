@echo off
"C:\Users\ismai\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r "%~dp0requirements.txt"
"C:\Users\ismai\AppData\Local\Programs\Python\Python312\python.exe" -m streamlit run "%~dp0app.py"
pause
