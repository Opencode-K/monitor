from cgi import print_arguments
from flask import Blueprint, Response, stream_with_context
import os, cv2, time
from app.services.camera_service   import read_cameras
from app.services.detection_service import detect_fire, detect_smoke, detect_temperature, detect_helmets

stream_bp = Blueprint('stream', __name__)

VIDEO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../local_videos'))
MODEL_MAP = {
    '火灾检测': detect_fire,
    '烟雾检测': detect_smoke,
    '异常温度': detect_temperature,
    '人员佩戴': detect_helmets
}

@stream_bp.route('/stream/<name>', methods=['GET'])
def stream(name):
    print(f"[STREAM] 请求 camera：{name}", flush=True)
    cams = read_cameras()
    cam = next((c for c in cams if c['name']==name), None)
    if not cam:
        print("[STREAM] 未找到对应摄像头", flush=True)
        return "Camera not found", 404
    # 拼本地文件路径同 results 逻辑
    src = cam['video']
    if src.startswith('/api/cameras/video/') or src.startswith('/video/'):
        # 本地文件
        fname = src.rsplit('/',1)[-1]
        path  = os.path.join(VIDEO_DIR, fname)
    elif src.startswith('http://') or src.startswith('https://'):
        # 网络摄像头：补齐 /stream
        path = src.rstrip('/') + '/stream'
    else:
        path = src


    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    def gen():
        frame_idx = 0
        while True:
            t0 = time.time()            
            ret, frame = cap.read()
            t1 = time.time()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            for task in cam.get('tasks', []):
                fn = MODEL_MAP.get(task)
                if fn:
                    frame, _ = fn(frame)
            t2 = time.time()
            _, jpg = cv2.imencode('.jpg', frame)
            t3 = time.time()
            if frame_idx % 100 == 0:
                print(f"[STREAM] read={(t1-t0)*1000:.1f}ms, infer={(t2-t1)*1000:.1f}ms, encode={(t3-t2)*1000:.1f}ms")
            frame_idx += 1
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'+jpg.tobytes()+b'\r\n')
            time.sleep(0.03)
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
