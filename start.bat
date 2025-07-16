@echo off
REM AI Search Engine Startup Script for Windows
REM This script starts both the backend API and frontend

echo 🚀 Starting AI Search Engine...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd frontend
npm install
cd ..

REM Start backend in background
echo 🔧 Starting backend API...
start "Backend API" python backend/run_server.py

REM Wait for backend to start
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend
echo 🎨 Starting frontend...
cd frontend
start "Frontend" npm start
cd ..

echo.
echo 🎉 AI Search Engine is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul 