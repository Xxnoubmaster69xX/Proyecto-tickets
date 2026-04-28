#!/bin/bash

echo "========================================="
echo "   Iniciando Ticket de Turno Web UI      "
echo "========================================="

# Iniciar backend
echo "[1/2] Iniciando Backend FastAPI (Puerto 8000)..."
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Iniciar frontend
echo "[2/2] Iniciando Frontend React/Vite (Puerto 5173)..."
cd frontend
export PATH=/opt/homebrew/bin:$PATH
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=== SISTEMA EN LÍNEA ==="
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000/docs"
echo "Presiona Ctrl+C para detener ambos servidores."

# Capturar Ctrl+C para limpiar
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM

wait
