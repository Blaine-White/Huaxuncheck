import pandas as pd
from flask import request
from ..models import Device
from ..models.base import db
from ..utils.validation import validate_device_data, create_error_response, create_success_response

class ImportService:
    """导入服务类"""
    
    def __init__(self):
        pass
    
    def import_devices_from_excel(self, file):
        """从Excel文件导入设备"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file, sheet_name=0)
            
            # 验证必要的列
            required_columns = ['设备名称', 'IP地址', '用户名', '密码', '设备类型', '连接协议', '巡检命令']
            missing_columns = []
            
            for col in required_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                return create_error_response(f'Excel文件缺少必要的列: {", ".join(missing_columns)}')
            
            # 处理数据
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # 构建设备数据
                    device_data = {
                        'name': str(row['设备名称']).strip(),
                        'ip': str(row['IP地址']).strip(),
                        'username': str(row['用户名']).strip(),
                        'password': str(row['密码']).strip(),
                        'enable_password': str(row.get('Enable密码', '')).strip(),
                        'device_type': str(row['设备类型']).strip(),
                        'protocol': str(row['连接协议']).strip().lower(),
                        'commands': str(row['巡检命令']).strip(),
                        'group': str(row.get('设备分组', '交换机')).strip()
                    }
                    
                    # 数据验证
                    errors_list = validate_device_data(device_data)
                    if errors_list:
                        error_count += 1
                        errors.append(f'第{index + 2}行: {"; ".join(errors_list)}')
                        continue
                    
                    # 检查IP是否已存在
                    existing_device = Device.get_by_ip(device_data['ip'])
                    if existing_device:
                        error_count += 1
                        errors.append(f'第{index + 2}行: IP地址 {device_data["ip"]} 已存在')
                        continue
                    
                    # 创建设备
                    device = Device(
                        name=device_data['name'],
                        ip=device_data['ip'],
                        username=device_data['username'],
                        password=device_data['password'],
                        enable_password=device_data['enable_password'],
                        device_type=device_data['device_type'],
                        protocol=device_data['protocol'],
                        commands=device_data['commands'],
                        group=device_data['group']
                    )
                    
                    device.save()
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f'第{index + 2}行: {str(e)}')
            
            # 返回结果
            if success_count == 0:
                return create_error_response(f'导入失败，所有设备都有错误:\n' + '\n'.join(errors[:10]))
            
            message = f'导入完成！成功: {success_count}个，失败: {error_count}个'
            if errors and len(errors) <= 5:
                message += f'\n错误详情:\n' + '\n'.join(errors)
            elif errors:
                message += f'\n部分错误详情:\n' + '\n'.join(errors[:5]) + '\n...'
            
            return create_success_response({
                'success_count': success_count,
                'error_count': error_count,
                'errors': errors
            }, message)
            
        except Exception as e:
            return create_error_response(f'读取Excel文件失败: {str(e)}')