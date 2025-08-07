import json
import time
import logging
from datetime import datetime
import netmiko
from ..models import Device, InspectionRecord, InspectionLog
from ..models.base import db, tz
from ..utils.device_utils import get_device_type, parse_device_commands, format_inspection_result
from ..utils.validation import create_error_response, create_success_response

logger = logging.getLogger(__name__)

class InspectionService:
    """巡检服务类"""
    
    def __init__(self):
        pass
    
    def inspect_single_device(self, device_id):
        """单设备巡检"""
        device = Device.query.get_or_404(device_id)
        
        # 检查设备状态
        if not device.is_online():
            return create_error_response(
                f'设备 {device.name} ({device.ip}) 当前不在线，无法执行巡检'
            )
        
        try:
            # 创建巡检日志
            inspection_log = InspectionLog(
                total_devices=1,
                status='进行中'
            )
            
            device_detail = {
                'device_id': device.id,
                'device_name': device.name,
                'device_ip': device.ip,
                'status': '进行中',
                'message': '正在巡检...',
                'start_time': datetime.now(tz).isoformat()
            }
            
            inspection_log.set_details([device_detail])
            inspection_log.save()
            
            # 执行巡检
            result = self._execute_device_inspection(device, inspection_log, 0)
            
            if result['success']:
                return create_success_response(result['data'], '巡检完成')
            else:
                return create_error_response(result['message'])
                
        except Exception as e:
            logger.error(f"单设备巡检异常: {str(e)}")
            return create_error_response(f'巡检失败: {str(e)}')
    
    def batch_inspect_devices(self, device_ids):
        """批量设备巡检"""
        if not device_ids or not isinstance(device_ids, list):
            return create_error_response('请提供要巡检的设备ID列表')
        
        # 获取在线设备
        devices = Device.query.filter(
            Device.id.in_(device_ids), 
            Device.status == 'online'
        ).all()
        
        if not devices:
            return create_error_response('所选设备中没有在线设备，无法进行巡检')
        
        try:
            # 创建批量巡检日志
            inspection_log = InspectionLog(
                total_devices=len(devices),
                status='进行中'
            )
            
            device_details = []
            for device in devices:
                device_details.append({
                    'device_id': device.id,
                    'device_name': device.name,
                    'device_ip': device.ip,
                    'status': '等待中',
                    'message': '等待巡检...',
                    'start_time': None,
                    'end_time': None
                })
            
            inspection_log.set_details(device_details)
            inspection_log.save()
            
            # 执行批量巡检
            successful_count = 0
            failed_count = 0
            start_time = time.time()
            
            for idx, device in enumerate(devices):
                # 检查是否被取消
                current_log = InspectionLog.query.get(inspection_log.id)
                if current_log.status == '已取消':
                    logger.info(f"巡检任务 {inspection_log.id} 被用户取消")
                    break
                
                # 执行单个设备巡检
                result = self._execute_device_inspection(device, inspection_log, idx)
                
                if result['success']:
                    successful_count += 1
                else:
                    failed_count += 1
            
            # 完成巡检任务
            total_duration = time.time() - start_time
            inspection_log.complete(successful_count, failed_count, total_duration)
            
            return create_success_response({
                'inspection_log_id': inspection_log.id,
                'total_devices': len(devices),
                'successful_count': successful_count,
                'failed_count': failed_count,
                'duration': total_duration
            }, '批量巡检完成')
            
        except Exception as e:
            logger.error(f"批量巡检异常: {str(e)}")
            return create_error_response(f'批量巡检失败: {str(e)}')
    
    def _execute_device_inspection(self, device, inspection_log, device_index):
        """执行单个设备的巡检"""
        start_time = time.time()
        
        try:
            # 更新设备状态为进行中
            inspection_log.update_device_detail(device.id, 
                status='进行中',
                message='正在巡检...',
                start_time=datetime.now(tz).isoformat()
            )
            db.session.commit()
            
            # 获取设备类型
            device_type = get_device_type(device.device_type, device.protocol)
            logger.info(f"开始巡检设备: {device.name} ({device.ip}), 设备类型: {device_type}")
            
            # 建立连接
            connection_params = {
                'device_type': device_type,
                'host': device.ip,
                'username': device.username,
                'password': device.password,
                'timeout': 30,
                'auth_timeout': 30,
                'banner_timeout': 30,
                'fast_cli': False
            }
            
            # 添加enable密码
            if device.enable_password and device.enable_password.strip():
                connection_params['secret'] = device.enable_password
            
            # 连接设备
            logger.info(f"正在连接设备: {device.ip}")
            connection = netmiko.ConnectHandler(**connection_params)
            logger.info(f"成功连接到设备: {device.ip}")
            
            # 进入enable模式（如果需要）
            if 'cisco_ios' in device_type and device.enable_password and device.enable_password.strip():
                logger.info(f"正在进入enable模式: {device.ip}")
                connection.enable()
                logger.info(f"已进入enable模式: {device.ip}")
            elif 'ruijie_os' in device_type:
                logger.info(f"锐捷交换机设备 {device.ip} 不需要进入 enable 模式，跳过此步骤")
            
            # 解析并执行命令
            commands = parse_device_commands(device.commands)
            logger.info(f"设备 {device.ip} 的巡检命令: {commands}")
            
            command_results = []
            command_success = True
            
            for cmd in commands:
                try:
                    logger.info(f"设备 {device.ip} 执行命令: {cmd}")
                    output = connection.send_command(cmd, strip_prompt=False, strip_command=False)
                    command_results.append({
                        'command': cmd,
                        'output': output
                    })
                    logger.info(f"设备 {device.ip} 命令 {cmd} 执行成功")
                except Exception as e:
                    error_msg = f"执行命令 {cmd} 失败: {str(e)}"
                    logger.error(error_msg)
                    command_success = False
                    command_results.append({
                        'command': cmd,
                        'output': error_msg
                    })
            
            # 断开连接
            connection.disconnect()
            logger.info(f"已断开与设备 {device.ip} 的连接")
            
            # 保存巡检记录
            record = InspectionRecord(
                device_id=device.id,
                device_name=device.name,
                result=json.dumps(command_results, ensure_ascii=False)
            )
            record.save()
            logger.info(f"设备 {device.name} ({device.ip}) 巡检完成，已保存记录")
            
            # 更新设备详情
            end_time = datetime.now(tz).isoformat()
            inspection_log.update_device_detail(device.id,
                status='成功' if command_success else '失败',
                message='巡检完成' if command_success else '部分命令执行失败',
                end_time=end_time
            )
            db.session.commit()
            
            return {
                'success': True,
                'data': {
                    'results': command_results,
                    'record_id': record.id
                }
            }
            
        except netmiko.ssh_exception.NetMikoTimeoutException as e:
            error_msg = f'连接设备 {device.name} ({device.ip}) 超时: {str(e)}'
            logger.error(error_msg)
            return self._handle_inspection_error(device, inspection_log, error_msg)
            
        except netmiko.ssh_exception.NetMikoAuthenticationException as e:
            error_msg = f'设备 {device.name} ({device.ip}) 认证失败: {str(e)}'
            logger.error(error_msg)
            return self._handle_inspection_error(device, inspection_log, error_msg)
            
        except Exception as e:
            error_msg = f'巡检设备 {device.name} ({device.ip}) 时出错: {str(e)}'
            logger.error(error_msg)
            return self._handle_inspection_error(device, inspection_log, error_msg)
    
    def _handle_inspection_error(self, device, inspection_log, error_msg):
        """处理巡检错误"""
        try:
            # 更新设备详情
            inspection_log.update_device_detail(device.id,
                status='失败',
                message=error_msg,
                end_time=datetime.now(tz).isoformat()
            )
            db.session.commit()
            
            return {
                'success': False,
                'message': error_msg
            }
        except Exception as e:
            logger.error(f"处理巡检错误时出现异常: {str(e)}")
            return {
                'success': False,
                'message': f'处理错误时出现异常: {str(e)}'
            }
    
    def cancel_inspection(self, log_id):
        """取消巡检任务"""
        inspection_log = InspectionLog.query.get_or_404(log_id)
        
        if inspection_log.status != '进行中':
            return create_error_response('只能取消进行中的巡检任务')
        
        try:
            inspection_log.cancel()
            return create_success_response(message='巡检任务已取消')
        except Exception as e:
            return create_error_response(f'取消巡检任务失败: {str(e)}')
    
    def get_inspection_logs(self, limit=None):
        """获取巡检日志列表"""
        if limit:
            logs = InspectionLog.get_recent_logs(limit)
        else:
            logs = InspectionLog.query.order_by(InspectionLog.start_time.desc()).all()
        
        return [log.to_dict() for log in logs]
    
    def get_inspection_log_detail(self, log_id):
        """获取巡检日志详情"""
        inspection_log = InspectionLog.query.get_or_404(log_id)
        return inspection_log.to_dict()
    
    def delete_inspection_log(self, log_id):
        """删除巡检日志"""
        inspection_log = InspectionLog.query.get_or_404(log_id)
        
        try:
            inspection_log.delete()
            return create_success_response(message='巡检日志删除成功')
        except Exception as e:
            return create_error_response(f'删除巡检日志失败: {str(e)}')