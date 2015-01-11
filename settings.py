import os

PRIVATE_FILE_URL = '/media_private/'

TEMP_DIR = os.path.normpath('./temp/plainpodcast')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
