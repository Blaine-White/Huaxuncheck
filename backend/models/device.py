from datetime import datetime
from .base import db, BaseModel, tz

class Device(db.Model, BaseModel):
    """设备模型"""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    enable_password = db.Column(db.String(100), nullable=True)
    device_type = db.Column(db.String(100), nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    commands = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unknown')
    last_check = db.Column(db.DateTime, nullable=True)
    group = db.Column(db.String(50), default='交换机')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz))
    
    # 关联关系
    inspection_records = db.relationship('InspectionRecord', backref='device', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Device {self.name}({self.ip})>'
    
    def to_dict(self):
        """重写to_dict方法，包含特定字段处理"""
        return {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
            'enable_password': self.enable_password,
            'device_type': self.device_type,
            'protocol': self.protocol,
            'commands': self.commands,
            'status': self.status,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'group': self.group,
            'created_at': self.created_at.isoformat()
        }
    
    def is_online(self):
        """检查设备是否在线"""
        return self.status == 'online'
    
    def update_status(self, status):
        """更新设备状态"""
        self.status = status
        self.last_check = datetime.now(tz)
        db.session.commit()
    
    @classmethod
    def get_by_ip(cls, ip):
        """根据IP地址获取设备"""
        return cls.query.filter_by(ip=ip).first()
    
    @classmethod
    def get_by_group(cls, group):
        """根据分组获取设备列表"""
        return cls.query.filter_by(group=group).all()
    
    @classmethod
    def get_online_devices(cls):
        """获取所有在线设备"""
        return cls.query.filter_by(status='online').all()