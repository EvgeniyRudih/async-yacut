import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///yacut.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    YADISK_API_URL = 'https://cloud-api.yandex.net'
    YADISK_UPLOAD_PATH = '/yacut/{}'
