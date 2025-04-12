from flask import Blueprint, jsonify, request

test_error_blueprint = Blueprint('test_read', __name__)

@test_error_blueprint.route('/file-read', methods=['POST'])
def read_uploaded_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    try:
        content = file.read().decode('utf-8')
        return jsonify({"filename": file.filename,"content": content})
    except FileNotFoundError as e:
        return jsonify({"error": "File not found", "filename": filename, "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "filename": filename, "details": str(e)}), 500
    