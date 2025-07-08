#!/bin/sh
set -e

DB_PATH="/usr/src/app/bibliodrive/data/db.sqlite3"
LOCAL_DB="/usr/src/app/bibliodrive/db.sqlite3.local"
FIXTURES="/usr/src/app/bibliodrive/all_fixtures.json"

# Crée le dossier data s'il n'existe pas
mkdir -p /usr/src/app/bibliodrive/data

# Si le fichier local existe et que le volume est vide, copie la base locale dans le volume
if [ ! -f "$DB_PATH" ] && [ -f "$LOCAL_DB" ]; then
  echo "[Entrypoint] Copie de la base locale initiale dans le volume Docker..."
  cp "$LOCAL_DB" "$DB_PATH"
fi

# Si la base n'existe toujours pas, crée-la via les migrations
if [ ! -f "$DB_PATH" ]; then
  echo "[Entrypoint] Base SQLite absente, création et initialisation..."
  python manage.py makemigrations
  python manage.py migrate
  if [ -f "$FIXTURES" ]; then
    python manage.py loaddata "$FIXTURES"
  fi
  
  # Crée un superuser Django
  echo "[Entrypoint] Création du superuser admin..."
  python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'admin123')
    print('Superuser admin créé avec succès')
else:
    print('Superuser admin existe déjà')
"
fi

exec "$@"