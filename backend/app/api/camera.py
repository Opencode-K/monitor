# backend/app/api/camera.py

from flask import Blueprint, jsonify, request, send_from_directory, current_app
from app.services.camera_service import (
    read_cameras,
    write_cameras,
    delete_camera_by_name,
    CONFIG_PATH, 
)
import os
import glob
import json

camera_bp = Blueprint('camera', __name__)

VIDEO_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../local_videos')
)




@camera_bp.record_once
def _log_local_videos(state):       
    files = [
        os.path.basename(p)
        for p in glob.glob(os.path.join(VIDEO_DIR, '*'))
    ]
    state.app.logger.info(
        "[serve_video] local_videos contains: %s", files
    )

@camera_bp.route('/', methods=['GET'])
def list_cameras():
    return jsonify(read_cameras())


@camera_bp.route('/<name>', methods=['GET'])
def get_camera(name):
    cams = read_cameras()
    cam = next((c for c in cams if c['name'] == name), None)
    if not cam:
        return jsonify({'msg': 'not found'}), 404
    return jsonify(cam)


@camera_bp.route('/video/<path:filename>', methods=['GET'])
def serve_video(filename):
    path = os.path.join(VIDEO_DIR, filename)
    if not os.path.isfile(path):
        current_app.logger.warning(f"[serve_video] Video not found: {path}")
        return "Not Found", 404
    return send_from_directory(VIDEO_DIR, filename, as_attachment=False)


@camera_bp.route('/', methods=['POST'])
def add_camera():
    data = request.get_json()
    write_cameras(data)
    return jsonify({'status': 'ok'})


@camera_bp.route('/<name>', methods=['DELETE'])
def delete_camera(name):
    delete_camera_by_name(name)
    return jsonify({'status': 'deleted'})


@camera_bp.route('/<name>', methods=['PUT'])
def update_camera(name):
    new_data = request.get_json()
    cameras = read_cameras()
    updated = False
    for i, cam in enumerate(cameras):
        if cam['name'] == name:
            cameras[i] = new_data
            updated = True
            break

    if not updated:
        return jsonify({'error': 'not found'}), 404

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cameras, f, ensure_ascii=False, indent=2)
    return jsonify({'status': 'updated'})
