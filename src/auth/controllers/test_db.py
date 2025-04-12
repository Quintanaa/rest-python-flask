from sqlite3 import IntegrityError
from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, IntegrityError

db_errors_blueprint = Blueprint('db_errors', __name__)

#Simulamos una mala conexión a la base de datos
BAD_DB_URI = 'sqlite:///non_existent_path/fake.db' #Intencionalmente incorrecta

@db_errors_blueprint.route('/db-connection-error', methods=['GET'])
def db_connection_error():
    """
    Simulamos un error de conexión a la base de datos
    """
    try:
        engine = create_engine(BAD_DB_URI)
        with engine.connect() as connection:
            conn.execute(text("SELECT 1"))
            # Si la conexión es exitosa, ejecutamos una consulta simple
            return jsonify({"message": "Database connection successful"})
    except OperationalError as e:
        return jsonify({"error": "Database connection error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    
@db_errors_blueprint.route('/db-query-error', methods=['GET'])
def db_query_error():
    """
    Consulta a tabla que no existe (simulando un error de consulta)
    """
    try:
        engine = create_engine('sqlite:///./test.db') #Usamos una base de datos SQLite para pruebas (debería funcionar)
        with engine.connect() as connection:
            # Intentamos insertar un registro duplicado
            connection.execute(text("SELECT * FROM tabla_que_no_existe")) #Simulamos una tabla que no existe
            # Si la consulta es exitosa, significa que no hubo error de clave única
            return jsonify({"message": "Database operation successful"})
    except OperationalError as e:
        return jsonify({"error": "Database operation error (no existe la tabla)", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    
@db_errors_blueprint.route('/db-unique-key-error', methods=['GET'])
def db_unique_key_error():
    """
    Simulamos un error de clave única en la base de datos
    """
    try:
        engine = create_engine('sqlite:///./test.db') #Usamos una base de datos SQLite para pruebas (debería funcionar)
        metadata = MetaData()
        # Definimos una tabla de ejemplo con una clave única
        users_table = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('userbame', String, unique=True)
        )

        metadata.create_all(engine) #Crea la tabla en la base de datos
        with engine.connect() as connection:
            # Intentamos insertar un registro duplicado
            connection.execute(text("INSERT INTO users (id, name) VALUES (1, 'Juan')"))
            connection.execute(text("INSERT INTO users (id, name) VALUES (2, 'Juan')"))
            # Si la consulta es exitosa, significa que no hubo error de clave única
            return jsonify({"message": "Database operation successful"})
    except IntegrityError as e:
        return jsonify({"error": "Database operation error (clave única)", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
