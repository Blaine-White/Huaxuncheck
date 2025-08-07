from flask import Blueprint, request, jsonify
from ..services import InspectionService

inspection_bp = Blueprint('inspection', __name__)
inspection_service = InspectionService()

@inspection_bp.route('/devices/<int:device_id>/inspect', methods=['POST'])
def inspect_device(device_id):
    """单设备巡检"""
    return inspection_service.inspect_single_device(device_id)

@inspection_bp.route('/devices/batch-inspect', methods=['POST'])
def batch_inspect_devices():
    """批量设备巡检"""
    data = request.json
    if not data or not data.get('device_ids'):
        return jsonify({
            'success': False,
            'message': '请提供要巡检的设备ID列表'
        }), 400
    
    return inspection_service.batch_inspect_devices(data['device_ids'])

@inspection_bp.route('/inspection-logs', methods=['GET'])
def get_inspection_logs():
    """获取巡检日志列表"""
    limit = request.args.get('limit', type=int)
    logs = inspection_service.get_inspection_logs(limit)
    return jsonify(logs)

@inspection_bp.route('/inspection-logs/<int:log_id>', methods=['GET'])
def get_inspection_log_detail(log_id):
    """获取巡检日志详情"""
    log_detail = inspection_service.get_inspection_log_detail(log_id)
    return jsonify(log_detail)

@inspection_bp.route('/inspection-logs/<int:log_id>', methods=['DELETE'])
def delete_inspection_log(log_id):
    """删除巡检日志"""
    return inspection_service.delete_inspection_log(log_id)

@inspection_bp.route('/inspection-logs/<int:log_id>/cancel', methods=['POST'])
def cancel_inspection(log_id):
    """取消巡检任务"""
    return inspection_service.cancel_inspection(log_id)