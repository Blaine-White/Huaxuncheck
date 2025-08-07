import re
from flask import jsonify

def validate_ip_address(ip):
    """验证IP地址格式"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    # 检查每个数字是否在0-255范围内
    parts = ip.split('.')
    for part in parts:
        if int(part) > 255:
            return False
    
    return True

def validate_device_data(data):
    """验证设备数据"""
    errors = []
    
    # 必填字段检查
    required_fields = ['name', 'ip', 'username', 'password', 'device_type', 'protocol', 'commands']
    for field in required_fields:
        if not data.get(field):
            errors.append(f'{field} 是必填字段')
    
    # IP地址格式检查
    if data.get('ip') and not validate_ip_address(data['ip']):
        errors.append('IP地址格式不正确')
    
    # 协议检查
    if data.get('protocol') and data['protocol'].lower() not in ['ssh', 'telnet']:
        errors.append('协议只能是SSH或Telnet')
    
    # 设备类型检查
    valid_device_types = [
        'cisco_ios', 'huawei', 'hp_comware', 'ruijie_os',
        'cisco_ios_telnet', 'huawei_telnet', 'hp_comware_telnet', 'ruijie_os_telnet'
    ]
    if data.get('device_type') and data['device_type'] not in valid_device_types:
        errors.append('设备类型不支持')
    
    return errors

def validate_inspection_data(data):
    """验证巡检数据"""
    errors = []
    
    if not data.get('device_ids') or not isinstance(data['device_ids'], list):
        errors.append('device_ids 必须是设备ID列表')
    
    if data.get('device_ids') and len(data['device_ids']) == 0:
        errors.append('至少需要选择一个设备')
    
    return errors

def create_error_response(message, status_code=400):
    """创建错误响应"""
    return jsonify({
        'success': False,
        'message': message
    }), status_code

def create_success_response(data=None, message='操作成功'):
    """创建成功响应"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)