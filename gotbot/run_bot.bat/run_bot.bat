@echo off
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -r requirements.txt

echo [*] Launching bot.py...
python bot.py

echo.
echo [!] Bot exited. Press any key to close this window.
pause >nul