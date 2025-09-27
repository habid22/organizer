#!/bin/bash

# Downloads Organizer - Development Startup Script
echo "🚀 Starting Downloads Organizer in Development Mode..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Create downloads directory if it doesn't exist
mkdir -p downloads

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your settings before running again."
    exit 0
fi

# Start backend
echo "🐍 Starting Python backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting React frontend..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo "✅ Downloads Organizer is running in development mode!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user to stop
wait $BACKEND_PID $FRONTEND_PID
