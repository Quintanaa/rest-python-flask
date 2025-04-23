import os
from flask import Flask, escape, request, jsonify 
from marshmallow import ValidationError
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.hash import bcrypt
import jwt
import datetime

from src.auth.auth_exception import UserExistsException, UserNotFoundException, AccessDeniedException
from src.auth.controllers.auth import auth_blueprint
from src.secret.controllers.secret import secret_blueprint
from src.auth.controllers.test_ficheros import test_error_blueprint
from src.auth.controllers.test_db import db_errors_blueprint
from src.auth.controllers.pokemon_api import pokemon_api_blueprint


app = Flask(__name__)
#PostgreSQL
POSTGRE_URL = "postgresql+psycopg2://postgres:425d@localhost:5432/flask_test"
postgre_engine = create_engine(POSTGRE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=postgre_engine)
Base = declarative_base()

#JWT secret key
JWT_SECRET_KEY = "contraseña"

#User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=postgre_engine)

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
        with postgre_engine.connect() as connection:
            result = connection.execute(text("SELECT datname FROM pg_database;"))
            return jsonify({"message": "Database is reachable", "result": [row[0] for row in result]})
    except Exception as e:
        return jsonify({"error": "Database connection error", "details": str(e)}), 500
    
@app.route(f'{prefix}/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    db = SessionLocal()

    if db.query(User).filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.hash(password)

    new_user = User(username=data["username"], email=data["email"], password=hashed_password)

    db.add(new_user)
    db.commit()
    db.close()
    return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201
    
@app.route(f'{prefix}/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    db = SessionLocal()

    user = db.query(User).filter_by(username=data['username']).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.verify(data['password'], user.password):
        return jsonify({"error": "Invalid password"}), 401

    token = jwt.encode({"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, JWT_SECRET_KEY, algorithm="HS256")

    db.close()
    return jsonify({"token": token}), 200
