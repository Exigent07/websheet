import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.path.join(
        os.environ.get('FLASK_INSTANCE_PATH', os.path.join(os.path.dirname(__file__), 'instance')), 
        'site.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
