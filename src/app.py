import os
from flask import Flask, escape, request, jsonify
from marshmallow import ValidationError
from flask_pymongo import PyMongo
from sqlalchemy import create_engine, text

from src.auth.auth_exception import UserExistsException, UserNotFoundException, AccessDeniedException
from src.auth.controllers.auth import auth_blueprint

import src.settings
from src.secret.controllers.secret import secret_blueprint
from src.auth.controllers.test_ficheros import test_error_blueprint
from src.auth.controllers.test_db import db_errors_blueprint


app = Flask(__name__)
#PostgreSQL
POSTGRE_URL = "postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/flask_test"
postgre_engine = create_engine(POSTGRE_URL)

app.config["MONGO_URI"] = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/db')

print(os.environ.get('MONGO_URL'))

mongo = PyMongo(app)

# set default version to v1
version = os.environ.get('API_VERSION', 'v1')
 
prefix = f"/api/{version}"


@app.errorhandler(ValidationError)
def validation_error_handler(err):
    errors = err.messages
    return jsonify(errors), 400


@app.errorhandler(UserExistsException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 400


@app.errorhandler(AccessDeniedException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 401


@app.errorhandler(UserNotFoundException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 404


app.register_blueprint(auth_blueprint, url_prefix=f'{prefix}/auth')

app.register_blueprint(secret_blueprint, url_prefix=f'{prefix}/secret')

app.register_blueprint(test_error_blueprint, url_prefix=f'{prefix}/file')

app.register_blueprint(db_errors_blueprint, url_prefix=f'{prefix}/db')


@app.route(f'{prefix}/ping', methods=['GET'])
def ping():
    """
        Check if server is alive
        :return: "pong"
    """
    return "pong"

@app.route(f'{prefix}/db-check', methods=['GET'])
def db_check():
    try:
        with postgre_engine.connect() as connection:
            result = connection.execute(text("SELECT datname FROM pg_database;"))
            return jsonify({"message": "Database is reachable", "result": [row[0] for row in result]})
    except Exception as e:
        return jsonify({"error": "Database connection error", "details": str(e)}), 500