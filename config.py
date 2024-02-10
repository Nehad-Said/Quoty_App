import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secrets_are_always_complicated'
	SQL_DB_USR = os.environ.get('SQL_DB_USR')
	SQL_DB_PWD = os.environ.get('SQL_DB_PWD')
	SQL_DB = os.environ.get('SQL_DB')
	SQL_HOST = os.environ.get('SQL_HOST') or 'localhost'
	SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://{SQL_DB_USR}:{SQL_DB_PWD}@{SQL_HOST}/{SQL_DB}'
	SQLALCHEMY_TRACK_MODIFICATIONS = False