from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app.services.user_service import create_user, authenticate_user
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    user = data.get('username', '').strip()
    pwd  = data.get('password', '')
    # 用户名：3–20位，字母/数字/下划线
    if not re.fullmatch(r'^[A-Za-z0-9_]{3,20}$', user):
        return jsonify({'msg':'用户名应为3-20位,由字母、数字或下划线组成'}), 400
    # 密码：至少6位，需同时包含字母和数字
    if len(pwd) < 6 or not re.search(r'[A-Za-z]', pwd) or not re.search(r'\d', pwd):
        return jsonify({'msg':'密码至少6位,且必须包含字母和数字'}), 400
    
    if not user or not pwd:
        return jsonify({'msg':'用户名和密码必填'}), 400
    if not create_user(user, pwd):
        return jsonify({'msg':'用户名已存在'}), 409
    return jsonify({'msg':'注册成功'}), 201
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = data.get('username','').strip()
    pwd  = data.get('password','').strip()
    if authenticate_user(user, pwd):
        token = create_access_token(identity=user)
        return jsonify(access_token=token), 200
    return jsonify({'msg':'用户名或密码错误'}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    return jsonify({'username': get_jwt_identity()})
