import platform
import subprocess
import logging
from datetime import datetime
from ..models.base import db, tz

logger = logging.getLogger(__name__)

def get_device_type(device_type, protocol):
    """根据设备类型和协议返回netmiko设备类型"""
    if protocol.lower() == 'telnet':
        return f"{device_type}_telnet"
    return device_type

def check_device_status(device):
    """检查设备状态"""
    try:
        # 根据操作系统选择ping命令
        if platform.system().lower() == 'windows':
            ping_cmd = f'ping -n 1 -w 1000 {device.ip}'
        else:
            ping_cmd = f'ping -c 1 -W 1 {device.ip}'
            
        result = subprocess.run(ping_cmd, shell=True, capture_output=True, text=True)
        status = 'online' if result.returncode == 0 else 'offline'
        device.update_status(status)
        return status
    except Exception as e:
        logger.error(f"检查设备 {device.ip} 状态时出错: {str(e)}")
        device.update_status('offline')
        return 'offline'

def check_all_devices_status(devices):
    """批量检查设备状态"""
    results = {}
    for device in devices:
        status = check_device_status(device)
        results[device.id] = status
    return results

def parse_device_commands(commands_str):
    """解析设备命令字符串"""
    import json
    
    try:
        # 尝试解析命令
        if commands_str.startswith('[') and commands_str.endswith(']'):
            # 如果命令是JSON数组格式
            commands_list = json.loads(commands_str)
            commands = [str(cmd).strip() for cmd in commands_list if cmd]
        else:
            # 如果不是JSON格式，尝试按逗号分隔
            commands = [cmd.strip() for cmd in commands_str.split(',') if cmd.strip()]
    except json.JSONDecodeError:
        # 如果JSON解析失败，尝试按逗号分隔处理
        commands = [cmd.strip() for cmd in commands_str.split(',') if cmd.strip()]
    except Exception as e:
        logger.error(f"命令解析错误: {str(e)}")
        commands = [commands_str] if commands_str else []
    
    # 确保commands是列表类型且每个命令都是纯文本字符串
    if not isinstance(commands, list):
        commands = [str(commands)] if commands else []
    else:
        commands = [str(cmd) for cmd in commands]
    
    # 清理命令，移除所有可能的特殊字符和格式
    cleaned_commands = []
    for cmd in commands:
        # 移除所有可能的引号（单引号和双引号）
        cmd = cmd.replace('"', '').replace("'", '')
        # 移除所有可能的方括号
        cmd = cmd.replace('[', '').replace(']', '')
        # 移除命令前后的空白字符
        cmd = cmd.strip()
        # 如果命令不为空，添加到清理后的命令列表
        if cmd:
            cleaned_commands.append(cmd)
    
    return cleaned_commands

def format_inspection_result(commands, outputs):
    """格式化巡检结果"""
    formatted_results = []
    
    for i, (command, output) in enumerate(zip(commands, outputs)):
        formatted_results.append({
            'command': command,
            'output': output,
            'index': i + 1
        })
    
    return formatted_results