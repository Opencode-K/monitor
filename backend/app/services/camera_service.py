import json, os
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../cameras.json')

def read_cameras():
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_cameras(new_cam):
    data = read_cameras()
    data.append(new_cam)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def delete_camera_by_name(name):
    data = read_cameras()
    data = [cam for cam in data if cam['name'] != name]
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
