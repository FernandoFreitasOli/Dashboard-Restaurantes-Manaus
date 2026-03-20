#!/bin/bash

# Script para instalar e rodar o Dashboard em React

echo "📦 Instalando dependências do Frontend..."
cd frontend
npm install

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "Para rodar a aplicação:"
echo ""
echo "Terminal 1 (Backend - Flask):"
echo "  source .venv/bin/activate"
echo "  python api.py"
echo ""
echo "Terminal 2 (Frontend - React):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "A aplicação estará disponível em: http://localhost:3000"
