from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

# 设置时区
tz = pytz.timezone('Asia/Shanghai')

class BaseModel:
    """基础模型类，提供通用字段和方法"""
    
    def to_dict(self):
        """将模型实例转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat() if value else None
            else:
                result[column.name] = value
        return result
    
    def save(self):
        """保存模型实例到数据库"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """从数据库删除模型实例"""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新模型实例"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self