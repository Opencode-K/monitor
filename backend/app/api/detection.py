# backend/app/api/detection.py

import os
from flask import Blueprint, jsonify, current_app, request
from app.services.camera_service import read_cameras
from app.services.detection_service import (
    detect_fire, detect_smoke, detect_temperature, detect_helmets
)
from app.services.alarm_service import write_alarm

# Blueprint

det_bp = Blueprint('detection', __name__)

# 任务到函数映射
MODEL_MAP = {
    '火灾检测': detect_fire,
    '烟雾检测': detect_smoke,
    '异常温度': detect_temperature,
    '人员佩戴': detect_helmets
}
# 报警过滤映射
TASK_LABEL = {
    '火灾检测': 'Fire',
    '烟雾检测': 'Smoke',
    '异常温度': 'TempHigh',
    '人员佩戴': 'Helmet'
}

@det_bp.route('/results/<name>')
def results(name):
    # 读取共享帧缓存与锁，若不存在则无需引入模块
    try:
        from app.api.stream import _frames, _locks
    except ImportError:
        _frames, _locks = {}, {}

    # 查找摄像头配置
    cams = read_cameras()
    cam = next((c for c in cams if c['name'] == name), None)
    if not cam:
        return jsonify([]), 404

    # 从共享缓存获取最新帧
    lock = _locks.get(name)
    if not lock:
        return jsonify([]), 200
    with lock:
        frame = _frames.get(name)
    if frame is None:
        return jsonify([]), 200

    # 对最新帧进行多任务检测
    all_results = []
    for task_name in cam.get('tasks', []):
        fn = MODEL_MAP.get(task_name)
        if not fn:
            continue
        try:
            # 传入 frame.copy() 避免绘制干扰
            _, detections = fn(frame.copy())
            # 写报警
            expected = TASK_LABEL.get(task_name)
            for det in detections:
                if det['label'] == expected:
                    write_alarm({
                        'camera': name,
                        'task':   task_name,
                        'label':  det['label'],
                        'conf':   det['conf']
                    })
            all_results.extend(detections)
        except Exception as e:
            current_app.logger.error(f"[results] 任务 {task_name} 失败: {e}")

    return jsonify(all_results), 200


@det_bp.route('/alarms', methods=['GET', 'OPTIONS'])
def get_alarms():
    # CORS 预检
    if request.method == 'OPTIONS':
        return '', 200
    from app.services.alarm_service import read_alarms
    return jsonify(read_alarms()), 200
