# """
# WSGI config for socialmedia project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')

# application = get_wsgi_application()
import os
import sys

# Project directory
project_home = '/home/socialmediacodenicely/social-media'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'socialmedia.settings'

# Activate virtual environment
activate_this = '/home/socialmediacodenicely/social-media/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
