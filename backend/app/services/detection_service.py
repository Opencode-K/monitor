# backend/app/services/detection_service.py
import os
# 不自动下载 ultralytics release 资源（使用本地权重）
os.environ["YOLO_NO_AUTO_DOWNLOAD"] = "1"

import cv2
import torch
from ultralytics import YOLO
os.environ["YOLO_NO_AUTO_DOWNLOAD"] = "1"
# 运行设备
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.backends.cudnn.benchmark = True
# 模型文件路径
# BASE_DIR   = os.path.abspath(os.path.dirname(__file__))
BASE_DIR   = ""
MODEL_DIR  = os.path.join(BASE_DIR, 'model')
FIRE_MODEL   = os.path.join(MODEL_DIR, 'best_fire.pt')
SMOKE_MODEL  = os.path.join(MODEL_DIR, 'best_smoke.pt')
TEMP_MODEL   = os.path.join(MODEL_DIR, 'best_temp.pt')
HELMET_MODEL = os.path.join(MODEL_DIR, 'best_helmet.pt')
SLEEVE_MODEL = os.path.join(MODEL_DIR, 'best_sleeve.pt')

# 辅助函数：延迟加载模型并忽略下载失败
def _load_model(path):
    try:
        return YOLO(path)
    except Exception as e:
        current = os.path.basename(path)
        print(f"Warning: 无法加载模型 {current}: {e}")
        return None
        
# 只在第一次调用时加载
_fire_model   = _load_model(FIRE_MODEL)
_smoke_model  = _load_model(SMOKE_MODEL)
_temp_model   = _load_model(TEMP_MODEL)
_helmet_model = _load_model(HELMET_MODEL)
# _sleeve_model = _load_model(SLEEVE_MODEL)


def _infer(model: YOLO, frame, conf_threshold=0.3):
    if model is None:
        return [], [], [], {}

    # 转 RGB
    img =frame # cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 推理
    results = model(img, imgsz=640, conf=conf_threshold)[0]

    h, w = frame.shape[:2]
    xy_norm = results.boxes.xyxyn.cpu().numpy()  # normalized coords
    boxes = [(
        int(x1 * w), int(y1 * h),
        int(x2 * w), int(y2 * h)
    ) for x1, y1, x2, y2 in xy_norm]

    confs = results.boxes.conf.cpu().numpy().tolist()
    clses = results.boxes.cls.cpu().numpy().tolist()
    names = results.names
    return boxes, confs, clses, names


# 各任务 detector: 绘制框 & 标签

def detect_fire(frame):
    boxes, confs, clses, names = _infer(_fire_model, frame, conf_threshold=0.3)
    detections = []
    h, w = frame.shape[:2]
    color = (0, 0, 255)
    for (x1, y1, x2, y2), c, cl in zip(boxes, confs, clses):
        label = names[int(cl)]
        detections.append({"label": label, "conf": float(c)})
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {c*100:.1f}%", (x1, max(y1-5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    if detections:
        banner = "FIRE"
        fs, thk = 2.0, 4
        (tw, th), _ = cv2.getTextSize(banner, cv2.FONT_HERSHEY_SIMPLEX, fs, thk)
        x = (w - tw) // 2
        y = th + 10
        cv2.putText(frame, banner, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fs, color, thk)
    return frame, detections

def detect_smoke(frame):
    boxes, confs, clses, names = _infer(_smoke_model, frame, conf_threshold=0.3)
    detections = []
    color = (0, 0, 0)
    for (x1, y1, x2, y2), c, cl in zip(boxes, confs, clses):
        label = names[int(cl)]
        if(cl == 1):
            color = (255, 255, 255)
        detections.append({"label": label, "conf": float(c)})
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {c*100:.1f}%", (x1, max(y1-5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return frame, detections


def detect_temperature(frame):
    boxes, confs, clses, names = _infer(_temp_model, frame, conf_threshold=0.3)
    detections = []
    h, w = frame.shape[:2]
    color = (0, 0, 255)
    for (x1, y1, x2, y2), c, cl in zip(boxes, confs, clses):
        label = names[int(cl)]
        detections.append({"label": label, "conf": float(c)})
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {c*100:.1f}%", (x1, max(y1-5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    if detections:
        banner = "Hot"
        fs, thk = 2.0, 4
        (tw, th), _ = cv2.getTextSize(banner, cv2.FONT_HERSHEY_SIMPLEX, fs, thk)
        x = (w - tw) // 2
        y = th + 10
        cv2.putText(frame, banner, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fs, color, thk)
    return frame, detections


def detect_helmets(frame):
    boxes, confs, clses, names = _infer(_helmet_model, frame, conf_threshold=0.3)
    detections = []
    for (x1, y1, x2, y2), c, cl in zip(boxes, confs, clses):
        label = names[int(cl)]
        detections.append({"label": label, "conf": float(c)})
        color = (0, 255, 0) if int(cl) == 0 else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {c*100:.1f}%", (x1, max(y1-5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return frame, detections
