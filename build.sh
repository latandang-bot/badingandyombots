#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User=get_user_model(); u=os.environ.get('DJANGO_SUPERUSER_USERNAME'); e=os.environ.get('DJANGO_SUPERUSER_EMAIL'); p=os.environ.get('DJANGO_SUPERUSER_PASSWORD'); ( User.objects.filter(username=u).exists() or User.objects.create_superuser(u,e,p) ) if (u and e and p) else None"