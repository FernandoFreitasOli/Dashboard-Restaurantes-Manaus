#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -x ".venv/bin/python" ]; then
  echo "🐍 Criando ambiente virtual Python..."
  python3 -m venv .venv
fi

echo "📦 Instalando dependências do Backend..."
.venv/bin/python -m pip install -r requirements.txt

echo "📦 Instalando dependências do Frontend..."
cd frontend
npm install

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "Para rodar a aplicação:"
echo ""
echo "Terminal 1 (Backend - Flask):"
echo "  cd \"$ROOT_DIR\""
echo "  .venv/bin/python api.py"
echo ""
echo "Terminal 2 (Frontend - React):"
echo "  cd \"$ROOT_DIR/frontend\""
echo "  npm run dev"
echo ""
echo "A aplicação estará disponível em: http://localhost:3000"
