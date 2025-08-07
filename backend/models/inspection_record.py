from datetime import datetime
from .base import db, BaseModel, tz

class InspectionRecord(db.Model, BaseModel):
    """巡检记录模型"""
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz))
    
    def __repr__(self):
        return f'<InspectionRecord {self.device_name} - {self.created_at}>'
    
    def to_dict(self):
        """重写to_dict方法"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'device_name': self.device_name,
            'result': self.result,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def get_by_device(cls, device_id, limit=None):
        """根据设备ID获取巡检记录"""
        query = cls.query.filter_by(device_id=device_id).order_by(cls.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_recent_records(cls, limit=10):
        """获取最近的巡检记录"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()