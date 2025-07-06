# run.py
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from flask import send_from_directory
from app import create_app


app = create_app()
print(app.url_map)
# ← 这一段放在 app = create_app() 之后，if __name__ 之前
VIDEO_DIR = os.path.join(os.path.dirname(__file__), 'local_videos')
@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run(host="0.0.0.0", port=5000, debug=False)
