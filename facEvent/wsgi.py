"""
WSGI config for facEvent project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facEvent.settings')

application = get_wsgi_application()



# your_project/wsgi.py or your_project/asgi.py

from event.tasks import scheduler

application = get_wsgi_application()
scheduler.start()