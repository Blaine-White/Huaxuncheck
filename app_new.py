import os
import logging
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

# 导入配置
from backend.config.settings import config
from backend.models.base import db
from backend.routes import register_routes
from backend.services import DeviceService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # 注册路由
    register_routes(app)
    
    # 首页路由
    @app.route('/')
    def index():
        return send_from_directory('frontend_new', 'index.html')
    
    # 静态文件路由
    @app.route('/assets/<path:filename>')
    def assets(filename):
        return send_from_directory('frontend_new/assets', filename)
    
    @app.route('/components/<path:filename>')
    def components(filename):
        return send_from_directory('frontend_new/components', filename)
    
    @app.route('/services/<path:filename>')
    def services(filename):
        return send_from_directory('frontend_new/services', filename)
    
    @app.route('/utils/<path:filename>')
    def utils(filename):
        return send_from_directory('frontend_new/utils', filename)
    
    # 创建数据库表
    with app.app_context():
        try:
            db.create_all()
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"数据库表创建失败: {str(e)}")
            raise
    
    return app

def start_background_services(app):
    """启动后台服务"""
    with app.app_context():
        device_service = DeviceService()
        device_service.start_status_check()
        logger.info("设备状态检查服务已启动")

if __name__ == '__main__':
    app = create_app()
    
    # 启动后台服务
    start_background_services(app)
    
    # 启动应用
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"应用启动在端口 {port}")
    logger.info(f"调试模式: {debug}")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("应用停止")