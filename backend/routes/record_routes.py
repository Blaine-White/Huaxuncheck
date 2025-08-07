from flask import Blueprint, request, jsonify
from ..models import InspectionRecord
from ..utils.export_utils import export_records_to_excel, export_single_record_to_txt, export_batch_records_to_zip

record_bp = Blueprint('records', __name__)

@record_bp.route('/devices/<int:device_id>/records', methods=['GET'])
def get_device_records(device_id):
    """获取设备的巡检记录"""
    limit = request.args.get('limit', type=int)
    records = InspectionRecord.get_by_device(device_id, limit)
    return jsonify([record.to_dict() for record in records])

@record_bp.route('/records', methods=['GET'])
def get_all_records():
    """获取所有巡检记录"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = InspectionRecord.query.order_by(
        InspectionRecord.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'records': [record.to_dict() for record in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    })

@record_bp.route('/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """删除巡检记录"""
    record = InspectionRecord.query.get_or_404(record_id)
    
    try:
        record.delete()
        return jsonify({
            'success': True,
            'message': '巡检记录删除成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除巡检记录失败: {str(e)}'
        }), 500

@record_bp.route('/records/<int:record_id>/export', methods=['GET'])
def export_single_record(record_id):
    """导出单个巡检记录"""
    record = InspectionRecord.query.get_or_404(record_id)
    return export_single_record_to_txt(record)

@record_bp.route('/records/batch-export', methods=['GET'])
def batch_export_records():
    """批量导出巡检记录"""
    record_ids = request.args.getlist('record_ids', type=int)
    
    if not record_ids:
        return jsonify({
            'success': False,
            'message': '请选择要导出的记录'
        }), 400
    
    records = InspectionRecord.query.filter(InspectionRecord.id.in_(record_ids)).all()
    
    if not records:
        return jsonify({
            'success': False,
            'message': '没有找到要导出的记录'
        }), 404
    
    return export_batch_records_to_zip(records)

@record_bp.route('/records/export', methods=['GET'])
def export_all_records():
    """导出所有巡检记录到Excel"""
    records = InspectionRecord.query.order_by(InspectionRecord.created_at.desc()).all()
    return export_records_to_excel(records)