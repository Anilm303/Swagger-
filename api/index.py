import os
import sys

# project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# IMPORTANT: set settings BEFORE Django loads
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel expects "app"
app = application