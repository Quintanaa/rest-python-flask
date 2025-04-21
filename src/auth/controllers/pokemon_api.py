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
        return jsonify({"error": "Unauthorized access", "details": "You are not authorized to access this resource"}), 401
    elif error_type == 'forbidden':
        return jsonify({"error": "Forbidden access", "details": "You do not have permission to access this resource"}), 403
    elif error_type == 'not_found':
        return jsonify({"error": "Pokemon not found", "details": f"Pokemon '{pokemon_name}' not found"}), 404
    elif error_type == 'connection':
        return jsonify({"error": "Connection error", "details": "Failed to connect to the Pokemon API"}), 503
    elif error_type == 'timeout':
        return jsonify({"error": "Request timeout", "details": "The request to the Pokemon API timed out"}), 504
    elif error_type == 'bad_request':
        return jsonify({"error": "Bad request"}), 400
    elif error_type == 'internal_server_error':
        return jsonify({"error": "Internal server error"}), 500

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
    
    except HTTPError as http_err:
        if response.status_code == 401:
            return jsonify({"error": "Unauthorized access", "details": str(http_err)}), 401
        elif response.status_code == 403:
            return jsonify({"error": "Forbidden access", "details": str(http_err)}), 403
        elif response.status_code == 404:
            return jsonify({"error": "Pokemon not found", "details": str(http_err)}), 404
        else:
            return jsonify({"error": "HTTP error occurred", "details": str(http_err)}), 500
    except Timeout as timeout_err:
        return jsonify({"error": "Request timeout", "details": str(timeout_err)}), 504
    except ConnectionError as conn_err:
        return jsonify({"error": "Connection error", "details": str(conn_err)}), 503
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    
    