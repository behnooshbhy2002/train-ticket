# from django.contrib.auth.models import User

# def before_all(context):
#     # Set up test data
#     User.objects.create_user(username='zari2', password='123456789')

import os
import sys
import django

# Add the project root directory (where manage.py is located) to PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lttp.settings')
django.setup()

# from django.test.client import Client

# def before_scenario(context, scenario):
#     # Initialize the Django test client and attach it to the context
#     context.client = Client()

