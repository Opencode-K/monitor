# backend/app/__init__.py

from flask import Flask, request, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    # 全局允许带不带尾斜杠的路由，不走 301 重定向
    app.url_map.strict_slashes = False
    # 允许所有来源对 /api/* 进行跨域，放行常用方法和头
    CORS(
      app,
      resources={r"/api/*": {"origins": "*"}},
      supports_credentials=True,
      allow_headers=["Content-Type", "Authorization"],
      methods=["GET","HEAD","POST","OPTIONS","PUT","PATCH","DELETE"]
    )
    # 全局拦截 OPTIONS 预检请求，直接返回 200 OK
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS' and request.path.startswith('/api/'):
            return make_response(('', 200))
    # JWT 配置
    app.config['JWT_SECRET_KEY'] = 'change_this_to_a_strong_secret'
    JWTManager(app)




    # 注册认证路由
    from .api.auth import auth_bp
    from .api.camera import camera_bp
    from .api.detection import det_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')    
    app.register_blueprint(camera_bp, url_prefix='/api/cameras')


    from .api.stream import stream_bp

    app.register_blueprint(stream_bp, url_prefix='/api/detection')
    app.register_blueprint(det_bp, url_prefix='/api/detection')

    from .api.alarm import alarm_bp
    app.register_blueprint(alarm_bp)  
    
    

    return app
