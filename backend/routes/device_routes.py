from flask import Blueprint, request, jsonify
from ..services import DeviceService
from ..utils.export_utils import export_devices_to_excel

device_bp = Blueprint('devices', __name__)
device_service = DeviceService()

@device_bp.route('/devices', methods=['GET'])
def get_devices():
    """获取所有设备"""
    devices = device_service.get_all_devices()
    return jsonify(devices)

@device_bp.route('/devices', methods=['POST'])
def create_device():
    """创建新设备"""
    data = request.json
    if not data:
        return jsonify({
            'success': False,
            'message': '请提供设备数据'
        }), 400
    
    return device_service.create_device(data)

@device_bp.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    """更新设备"""
    data = request.json
    if not data:
        return jsonify({
            'success': False,
            'message': '请提供设备数据'
        }), 400
    
    return device_service.update_device(device_id, data)

@device_bp.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    """删除设备"""
    return device_service.delete_device(device_id)

@device_bp.route('/devices/export', methods=['GET'])
def export_devices():
    """导出设备信息到Excel"""
    from ..models import Device
    devices = Device.query.all()
    return export_devices_to_excel(devices)

@device_bp.route('/devices/groups', methods=['GET'])
def get_device_groups():
    """获取设备分组"""
    groups = device_service.get_device_groups()
    return jsonify(groups)

@device_bp.route('/devices/groups/<group_name>', methods=['GET'])
def get_devices_by_group(group_name):
    """根据分组获取设备"""
    devices = device_service.get_devices_by_group(group_name)
    return jsonify(devices)