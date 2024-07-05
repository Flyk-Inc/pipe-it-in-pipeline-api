from flask import Blueprint, request, jsonify
from app.consumer import process_message

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/process', methods=['POST'])
def process():
    data = request.json
    process_message(data)
    return jsonify({'status': 'success'}), 200
