from .device_routes import device_bp
from .inspection_routes import inspection_bp
from .record_routes import record_bp

def register_routes(app):
    """注册所有路由"""
    app.register_blueprint(device_bp, url_prefix='/api')
    app.register_blueprint(inspection_bp, url_prefix='/api')
    app.register_blueprint(record_bp, url_prefix='/api')

__all__ = ['register_routes']