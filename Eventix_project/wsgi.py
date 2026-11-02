"""
WSGI config for Eventix project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eventix_project.settings')

django_application = get_wsgi_application()

def application(environ, start_response):
    # Normalize path if Vercel serverless forwards the script path in PATH_INFO
    path_info = environ.get('PATH_INFO', '')
    if 'Eventix_project/wsgi.py' in path_info:
        cleaned_path = path_info.replace('/Eventix_project/wsgi.py', '').replace('Eventix_project/wsgi.py', '')
        environ['PATH_INFO'] = cleaned_path if cleaned_path else '/'
    return django_application(environ, start_response)

app = application
