import threading
import time
from ..models import Device
from ..models.base import db
from ..utils.device_utils import check_device_status
from ..utils.validation import validate_device_data, create_error_response, create_success_response

class DeviceService:
    """设备服务类"""
    
    def __init__(self):
        self.status_check_interval = None
        self._stop_status_check = False
    
    def get_all_devices(self):
        """获取所有设备"""
        devices = Device.query.all()
        return [device.to_dict() for device in devices]
    
    def get_device_by_id(self, device_id):
        """根据ID获取设备"""
        device = Device.query.get_or_404(device_id)
        return device
    
    def create_device(self, data):
        """创建新设备"""
        # 数据验证
        errors = validate_device_data(data)
        if errors:
            return create_error_response('; '.join(errors))
        
        # 检查IP是否已存在
        existing_device = Device.get_by_ip(data['ip'])
        if existing_device:
            return create_error_response(f'IP地址 {data["ip"]} 已存在')
        
        try:
            # 创建设备
            device = Device(
                name=data['name'],
                ip=data['ip'],
                username=data['username'],
                password=data['password'],
                enable_password=data.get('enable_password', ''),
                device_type=data['device_type'],
                protocol=data['protocol'],
                commands=data['commands'],
                group=data.get('group', '交换机')
            )
            
            device.save()
            
            # 立即检查设备状态
            check_device_status(device)
            
            return create_success_response(device.to_dict(), '设备添加成功')
            
        except Exception as e:
            return create_error_response(f'添加设备失败: {str(e)}')
    
    def update_device(self, device_id, data):
        """更新设备"""
        device = Device.query.get_or_404(device_id)
        
        # 数据验证
        errors = validate_device_data(data)
        if errors:
            return create_error_response('; '.join(errors))
        
        # 检查IP是否被其他设备使用
        if data['ip'] != device.ip:
            existing_device = Device.get_by_ip(data['ip'])
            if existing_device and existing_device.id != device_id:
                return create_error_response(f'IP地址 {data["ip"]} 已被其他设备使用')
        
        try:
            # 更新设备信息
            device.update(
                name=data['name'],
                ip=data['ip'],
                username=data['username'],
                password=data['password'],
                enable_password=data.get('enable_password', ''),
                device_type=data['device_type'],
                protocol=data['protocol'],
                commands=data['commands'],
                group=data.get('group', '交换机')
            )
            
            # 如果IP地址改变了，重新检查状态
            if data['ip'] != device.ip:
                check_device_status(device)
            
            return create_success_response(device.to_dict(), '设备更新成功')
            
        except Exception as e:
            return create_error_response(f'更新设备失败: {str(e)}')
    
    def delete_device(self, device_id):
        """删除设备"""
        device = Device.query.get_or_404(device_id)
        
        try:
            device.delete()
            return create_success_response(message='设备删除成功')
        except Exception as e:
            return create_error_response(f'删除设备失败: {str(e)}')
    
    def get_devices_by_group(self, group):
        """根据分组获取设备"""
        devices = Device.get_by_group(group)
        return [device.to_dict() for device in devices]
    
    def get_device_groups(self):
        """获取所有设备分组"""
        devices = Device.query.all()
        groups = set()
        for device in devices:
            if device.group:
                groups.add(device.group)
        return list(groups)
    
    def start_status_check(self):
        """启动设备状态检查"""
        if self.status_check_interval is None:
            self._stop_status_check = False
            self.status_check_interval = threading.Thread(target=self._check_all_devices_status)
            self.status_check_interval.daemon = True
            self.status_check_interval.start()
    
    def stop_status_check(self):
        """停止设备状态检查"""
        self._stop_status_check = True
        if self.status_check_interval:
            self.status_check_interval.join(timeout=1)
            self.status_check_interval = None
    
    def _check_all_devices_status(self):
        """检查所有设备状态（后台线程）"""
        while not self._stop_status_check:
            try:
                devices = Device.query.all()
                for device in devices:
                    if self._stop_status_check:
                        break
                    check_device_status(device)
                
                # 等待60秒后再次检查
                for _ in range(60):
                    if self._stop_status_check:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"设备状态检查出错: {str(e)}")
                time.sleep(10)  # 出错后等待10秒再重试