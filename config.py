"""Local-only coursework configuration; no original credentials are included."""
import os
from datetime import timedelta
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///coursework-demo.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
DEBUG = False
