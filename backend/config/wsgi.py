import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# ↓ この3行を新しく追加・修正します
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

