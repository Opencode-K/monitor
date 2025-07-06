# -*- coding: utf-8 -*-
import os
import json
import threading
from datetime import datetime

# 存放用户数据的文件
USER_PATH = os.path.join(os.path.dirname(__file__), '../../users.json')
_lock = threading.Lock()

def read_users():
    if not os.path.exists(USER_PATH):
        return []
    try:
        with open(USER_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        valid = []
        if isinstance(data, list):
            for u in data:
                if isinstance(u, dict) and 'username' in u and 'password' in u:
                    valid.append(u)
        return valid
    except (UnicodeDecodeError, json.JSONDecodeError):
        # 文件损坏，重置为空列表
        with open(USER_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []

def write_users(users):
    with _lock:
        with open(USER_PATH, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

def create_user(username: str, password: str) -> bool:
    users = read_users()
    if any(u['username'] == username for u in users):
        return False
    users.append({
        'username': username,
        'password': password,
        'created_at': datetime.utcnow().isoformat()
    })
    write_users(users)
    return True

def authenticate_user(username: str, password: str) -> bool:
    users = read_users()
    return any(u['username'] == username and u['password'] == password for u in users)
