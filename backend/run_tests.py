import os
import django
import unittest

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")  # Replace with your project path
django.setup()
loader = unittest.TestLoader()
tests = loader.discover('product/tests')
runner = unittest.TextTestRunner(verbosity=2)
runner.run(tests)
