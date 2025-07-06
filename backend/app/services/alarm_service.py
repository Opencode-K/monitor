  # backend/app/services/alarm_service.py
import os, json, threading, uuid
from datetime import datetime

ALARM_PATH = os.path.abspath(
  os.path.join(os.path.dirname(__file__), '../../alarms.json')
)
_lock = threading.Lock()

def read_alarms():
    if not os.path.exists(ALARM_PATH):
        return []
    try:
        with open(ALARM_PATH, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except (UnicodeDecodeError, json.JSONDecodeError):
        with open(ALARM_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []

def write_alarm(item: dict):
    """
    item: {camera, task, label, conf}
    """
    with _lock:
        alarms = read_alarms()
        record = {
            "id": str(uuid.uuid4()),
            **item,
            "time": datetime.utcnow().isoformat(),
            "ack": False
        }
        alarms.insert(0, record)
        alarms = alarms[:200]  # 最多保留 200 条
        with open(ALARM_PATH, 'w', encoding='utf-8') as f:
            json.dump(alarms, f, ensure_ascii=False, indent=2)

def ack_alarm(alarm_id: str):
    """将指定报警标记为已确认"""
    with _lock:
        alarms = read_alarms()
        for a in alarms:
            if a["id"] == alarm_id:
                a["ack"] = True
                break
        with open(ALARM_PATH, 'w', encoding='utf-8') as f:
            json.dump(alarms, f, ensure_ascii=False, indent=2)
        return a
