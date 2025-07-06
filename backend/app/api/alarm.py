# backend/app/api/alarm.py
from flask import Blueprint, jsonify, request
from app.services.alarm_service import read_alarms, write_alarm, ack_alarm

alarm_bp = Blueprint('alarm', __name__, url_prefix='/alarms')

@alarm_bp.route('', methods=['GET', 'OPTIONS'])
def list_alarms():
    return jsonify(read_alarms())

@alarm_bp.route('', methods=['POST'])
def create_alarm():
    data = request.get_json()
    write_alarm(data)
    return '', 204

@alarm_bp.route('/<alarm_id>/ack', methods=['PUT'])
def confirm_alarm(alarm_id):
    record = ack_alarm(alarm_id)
    if not record:
        return jsonify({"msg": "Not found"}), 404
    return jsonify(record)
