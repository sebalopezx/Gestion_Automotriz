#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate
# Recopilar archivos estáticos
python manage.py collectstatic --no-input
# Cargar datos
python manage.py loaddata data.json