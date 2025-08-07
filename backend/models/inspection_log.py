import json
from datetime import datetime
from .base import db, BaseModel, tz

class InspectionLog(db.Model, BaseModel):
    """巡检日志模型"""
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(tz))
    end_time = db.Column(db.DateTime, nullable=True)
    total_devices = db.Column(db.Integer, default=0)
    successful_devices = db.Column(db.Integer, default=0)
    failed_devices = db.Column(db.Integer, default=0)
    total_duration = db.Column(db.Float, default=0)  # 以秒为单位
    details = db.Column(db.Text, nullable=True)  # JSON格式存储详情
    status = db.Column(db.String(20), default='进行中')  # 进行中/已完成/已取消
    
    def __repr__(self):
        return f'<InspectionLog {self.id} - {self.status}>'
    
    def to_dict(self):
        """重写to_dict方法"""
        return {
            'id': self.id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'total_devices': self.total_devices,
            'successful_devices': self.successful_devices,
            'failed_devices': self.failed_devices,
            'total_duration': self.total_duration,
            'details': json.loads(self.details) if self.details else [],
            'status': self.status
        }
    
    def get_details(self):
        """获取详情信息"""
        return json.loads(self.details) if self.details else []
    
    def set_details(self, details):
        """设置详情信息"""
        self.details = json.dumps(details, ensure_ascii=False)
    
    def add_device_detail(self, device_detail):
        """添加设备详情"""
        details = self.get_details()
        details.append(device_detail)
        self.set_details(details)
    
    def update_device_detail(self, device_id, **kwargs):
        """更新设备详情"""
        details = self.get_details()
        for detail in details:
            if detail.get('device_id') == device_id:
                detail.update(kwargs)
                break
        self.set_details(details)
    
    def complete(self, successful_count, failed_count, duration):
        """完成巡检任务"""
        self.end_time = datetime.now(tz)
        self.successful_devices = successful_count
        self.failed_devices = failed_count
        self.total_duration = duration
        self.status = '已完成'
        db.session.commit()
    
    def cancel(self):
        """取消巡检任务"""
        self.end_time = datetime.now(tz)
        self.status = '已取消'
        db.session.commit()
    
    @classmethod
    def get_recent_logs(cls, limit=10):
        """获取最近的巡检日志"""
        return cls.query.order_by(cls.start_time.desc()).limit(limit).all()
    
    @classmethod
    def get_active_logs(cls):
        """获取进行中的巡检日志"""
        return cls.query.filter_by(status='进行中').all()