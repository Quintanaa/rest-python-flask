import os
from flask import Flask, jsonify 
from marshmallow import ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


from src.auth.auth_exception import UserExistsException, UserNotFoundException, AccessDeniedException
from src.auth.controllers.auth import auth_blueprint
from src.secret.controllers.secret import secret_blueprint
from src.auth.controllers.test_ficheros import test_error_blueprint
from src.auth.controllers.test_db import db_errors_blueprint
from src.auth.controllers.pokemon_api import pokemon_api_blueprint


app = Flask(__name__)
#MYSQL connection
MYSQL_URL = os.environ.get("MYSQL_URL", "mysql+pymysql://root:123456@localhost:3306/flask")
mysql_engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

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

app.register_blueprint(pokemon_api_blueprint, url_prefix=f'{prefix}/pokemon')


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
        with mysql_engine.connect() as connection:
            result = connection.execute(text("SHOW DATABASES;"))
            return jsonify({"message": "La base de datos es accesible", "result": [row[0] for row in result]})
    except Exception as e:
        return jsonify({"error": "Error de conexión a la base de datos", "details": str(e)}), 500
