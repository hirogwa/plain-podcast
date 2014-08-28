from django.conf import settings
import os

BASE_DIR = getattr(settings, 'BASE_DIR')
TEMPLATE_DIRS = getattr(settings, 'TEMPLATE_DIRS', [os.path.join(BASE_DIR, 'templates')])
PROJECT_ROOT = '/Users/hirogwa/Documents/workspace/uragakuya'

PRIVATE_FILE_ROOT = os.path.join(PROJECT_ROOT, 'media_private/')
PRIVATE_FILE_URL = '/media_private/'
