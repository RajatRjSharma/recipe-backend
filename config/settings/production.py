from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost', '13.127.195.54', 'ec2-13-127-195-54.ap-south-1.compute.amazonaws.com']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
