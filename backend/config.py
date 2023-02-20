import os
SECRET_KEY = os.urandom(32)

#basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:123@192.168.1.5:5432/trivia'
SQLALCHEMY_DATABASE_URI = 'sqlite:///trivia.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_ECHO = True

