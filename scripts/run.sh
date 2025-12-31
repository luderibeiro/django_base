#!/bin/sh

# Run the application
# Shell will fail if execution fails

set -e

echo "🚀 Iniciando aplicação Django..."

cd /app/project

# Executar migrações (makemigrations apenas se necessário)
echo "🗄️  Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar servidor
echo "✅ Aplicação pronta! Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
