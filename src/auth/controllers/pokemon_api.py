from flask import jsonify, request, Blueprint
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException

pokemon_api_blueprint = Blueprint('pokemon_api', __name__)


@pokemon_api_blueprint.route('/pokemon', methods=['GET'])
def get_pokemon():
    """
    Simulamos una consulta a la API de Pokemon
    """

    # Obtenemos el nombre del Pokemon desde los parámetros de la consulta
    pokemon_name = request.args.get('name', 'pikachu').lower()

    error_type = request.args.get('error', None)

    #Simulamos los diferentes tipos de errores
    if error_type == 'unauthorized':
        return jsonify({"error": "Acceso no autorizado", "details": "No estás autorizado para acceder a este recurso"}), 401
    elif error_type == 'forbidden':
        return jsonify({"error": "Acceso prohibido", "details": "No tienes permiso para acceder a este recurso"}), 403
    elif error_type == 'not_found':
        return jsonify({"error": "Pokemon no encontrado", "details": f"Pokemon '{pokemon_name}' no encontrado"}), 404
    elif error_type == 'connection':
        return jsonify({"error": "Error de conexión", "details": "No se pudo conectar a la API de Pokemon"}), 503
    elif error_type == 'timeout':
        return jsonify({"error": "Tiempo de espera agotado", "details": "La solicitud a la API de Pokemon agotó el tiempo de espera"}), 504
    elif error_type == 'bad_request':
        return jsonify({"error": "Solicitud incorrecta"}), 400
    elif error_type == 'internal_server_error':
        return jsonify({"error": "Error interno del servidor"}), 500

    try:
        #Respuesta de la API de Pokemon
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK

        # Procesamos la respuesta de la API
        data = response.json()
        simplified_data = {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [type_info["type"]["name"] for type_info in data["types"]],
            "abilities": [ability_info["ability"]["name"] for ability_info in data["abilities"]],
        }

        return jsonify({"pokemon":simplified_data})
    
    except HTTPError:
        if response.status_code == 401:
            return jsonify({"error": "Acceso no autorizado", "details": "No estás autorizado para acceder a este recurso"}), 401
        elif response.status_code == 403:
            return jsonify({"error": "Acceso prohibido", "details": "No tienes permiso para acceder a este recurso"}), 403
        elif response.status_code == 404:
            return jsonify({"error": "Pokemon no encontrado", "details": f"Pokemon '{pokemon_name}' no encontrado"}), 404
        else:
            return jsonify({"error": "Error interno del servidor"}), 500
    except Timeout:
        return jsonify({"error": "Tiempo de espera agotado", "details": "La solicitud a la API de Pokemon agotó el tiempo de espera"}), 504
    except ConnectionError:
        return jsonify({"error": "Error de conexión", "details": "No se pudo conectar a la API de Pokemon"}), 503
    except Exception:
        return jsonify({"error": "Error inesperado"}), 500
