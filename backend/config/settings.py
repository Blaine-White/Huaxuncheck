import os
from datetime import timedelta

class Config:
    """基础配置类"""
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///network_inspection.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'huaxuncheck-secret-key-2024'
    
    # 网络设备连接配置
    DEVICE_CONNECTION_TIMEOUT = 30
    DEVICE_AUTH_TIMEOUT = 30
    DEVICE_BANNER_TIMEOUT = 30
    
    # 巡检配置
    MAX_CONCURRENT_INSPECTIONS = 10
    INSPECTION_RETRY_COUNT = 3
    
    # 分页配置
    DEVICES_PER_PAGE = 10
    RECORDS_PER_PAGE = 10
    LOGS_PER_PAGE = 10
    
    # 时区配置
    TIMEZONE = 'Asia/Shanghai'
    
    # 支持的设备类型
    SUPPORTED_DEVICE_TYPES = {
        'cisco_ios': 'Cisco IOS',
        'cisco_ios_telnet': 'Cisco IOS (Telnet)',
        'huawei': 'Huawei VRP',
        'huawei_telnet': 'Huawei VRP (Telnet)',
        'hp_comware': 'H3C Comware',
        'hp_comware_telnet': 'H3C Comware (Telnet)',
        'ruijie_os': 'Ruijie OS',
        'ruijie_os_telnet': 'Ruijie OS (Telnet)',
    }
    
    # 默认设备分组
    DEFAULT_DEVICE_GROUPS = ['交换机', 'AP', 'PC', '路由器']

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_network_inspection.db'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}