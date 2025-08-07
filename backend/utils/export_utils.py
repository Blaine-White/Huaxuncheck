import io
import zipfile
from datetime import datetime
import pandas as pd
from flask import send_file

def export_devices_to_excel(devices):
    """导出设备信息到Excel"""
    # 准备数据
    data = []
    for device in devices:
        data.append({
            'ID': device.id,
            '设备名称': device.name,
            'IP地址': device.ip,
            '用户名': device.username,
            '密码': device.password,
            'Enable密码': device.enable_password or '',
            '设备类型': device.device_type,
            '连接协议': device.protocol,
            '巡检命令': device.commands,
            '设备分组': device.group,
            '设备状态': device.status,
            '最后检查时间': device.last_check.strftime('%Y-%m-%d %H:%M:%S') if device.last_check else '',
            '创建时间': device.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 创建Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='设备信息', index=False)
    
    output.seek(0)
    filename = f'设备信息_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def export_records_to_excel(records):
    """导出巡检记录到Excel"""
    # 准备数据
    data = []
    for record in records:
        data.append({
            'ID': record.id,
            '设备ID': record.device_id,
            '设备名称': record.device_name,
            '巡检结果': record.result,
            '巡检时间': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 创建Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='巡检记录', index=False)
    
    output.seek(0)
    filename = f'巡检记录_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def export_single_record_to_txt(record):
    """导出单个巡检记录为TXT文件"""
    content = f"""设备巡检报告
==========================================

设备信息：
- 设备名称：{record.device_name}
- 设备ID：{record.device_id}
- 巡检时间：{record.created_at.strftime('%Y-%m-%d %H:%M:%S')}

巡检结果：
==========================================
{record.result}

==========================================
报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    output = io.BytesIO()
    output.write(content.encode('utf-8'))
    output.seek(0)
    
    filename = f'{record.device_name}_巡检记录_{record.created_at.strftime("%Y%m%d_%H%M%S")}.txt'
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

def export_batch_records_to_zip(records):
    """批量导出巡检记录为ZIP文件"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for record in records:
            content = f"""设备巡检报告
==========================================

设备信息：
- 设备名称：{record.device_name}
- 设备ID：{record.device_id}
- 巡检时间：{record.created_at.strftime('%Y-%m-%d %H:%M:%S')}

巡检结果：
==========================================
{record.result}

==========================================
报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            filename = f'{record.device_name}_巡检记录_{record.created_at.strftime("%Y%m%d_%H%M%S")}.txt'
            zip_file.writestr(filename, content.encode('utf-8'))
    
    zip_buffer.seek(0)
    filename = f'批量巡检记录_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/zip'
    )