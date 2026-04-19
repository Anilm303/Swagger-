import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# FORCE settings BEFORE importing Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

app = application