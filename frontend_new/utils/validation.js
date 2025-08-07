// 前端验证工具函数

/**
 * 验证IP地址格式
 * @param {string} ip - IP地址
 * @returns {boolean} 是否有效
 */
function validateIPAddress(ip) {
    if (!ip || typeof ip !== 'string') return false;
    
    const pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!pattern.test(ip)) return false;
    
    const parts = ip.split('.');
    for (const part of parts) {
        const num = parseInt(part, 10);
        if (num > 255 || (part.length > 1 && part[0] === '0')) {
            return false;
        }
    }
    
    return true;
}

/**
 * 验证设备名称
 * @param {string} name - 设备名称
 * @returns {boolean} 是否有效
 */
function validateDeviceName(name) {
    if (!name || typeof name !== 'string') return false;
    return name.trim().length > 0 && name.length <= 100;
}

/**
 * 验证用户名
 * @param {string} username - 用户名
 * @returns {boolean} 是否有效
 */
function validateUsername(username) {
    if (!username || typeof username !== 'string') return false;
    return username.trim().length > 0 && username.length <= 50;
}

/**
 * 验证密码
 * @param {string} password - 密码
 * @returns {boolean} 是否有效
 */
function validatePassword(password) {
    if (!password || typeof password !== 'string') return false;
    return password.length > 0;
}

/**
 * 验证设备类型
 * @param {string} deviceType - 设备类型
 * @returns {boolean} 是否有效
 */
function validateDeviceType(deviceType) {
    const validTypes = [
        'cisco_ios', 'cisco_ios_telnet',
        'huawei', 'huawei_telnet',
        'hp_comware', 'hp_comware_telnet',
        'ruijie_os', 'ruijie_os_telnet'
    ];
    return validTypes.includes(deviceType);
}

/**
 * 验证协议
 * @param {string} protocol - 协议
 * @returns {boolean} 是否有效
 */
function validateProtocol(protocol) {
    return ['ssh', 'telnet'].includes(protocol?.toLowerCase());
}

/**
 * 验证命令字符串
 * @param {string} commands - 命令字符串
 * @returns {boolean} 是否有效
 */
function validateCommands(commands) {
    if (!commands || typeof commands !== 'string') return false;
    return commands.trim().length > 0;
}

/**
 * 验证设备分组
 * @param {string} group - 分组名称
 * @returns {boolean} 是否有效
 */
function validateGroup(group) {
    if (!group || typeof group !== 'string') return false;
    return group.trim().length > 0 && group.length <= 50;
}

/**
 * 验证完整的设备数据
 * @param {Object} deviceData - 设备数据
 * @returns {Object} 验证结果 {isValid: boolean, errors: string[]}
 */
function validateDeviceData(deviceData) {
    const errors = [];
    
    if (!validateDeviceName(deviceData.name)) {
        errors.push('设备名称不能为空且长度不超过100字符');
    }
    
    if (!validateIPAddress(deviceData.ip)) {
        errors.push('IP地址格式不正确');
    }
    
    if (!validateUsername(deviceData.username)) {
        errors.push('用户名不能为空且长度不超过50字符');
    }
    
    if (!validatePassword(deviceData.password)) {
        errors.push('密码不能为空');
    }
    
    if (!validateDeviceType(deviceData.device_type)) {
        errors.push('设备类型不支持');
    }
    
    if (!validateProtocol(deviceData.protocol)) {
        errors.push('协议只能是SSH或Telnet');
    }
    
    if (!validateCommands(deviceData.commands)) {
        errors.push('巡检命令不能为空');
    }
    
    if (deviceData.group && !validateGroup(deviceData.group)) {
        errors.push('分组名称格式不正确');
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

/**
 * 验证文件类型
 * @param {File} file - 文件对象
 * @param {string[]} allowedTypes - 允许的文件类型
 * @returns {boolean} 是否有效
 */
function validateFileType(file, allowedTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']) {
    if (!file) return false;
    return allowedTypes.includes(file.type);
}

/**
 * 验证文件大小
 * @param {File} file - 文件对象
 * @param {number} maxSize - 最大大小（字节）
 * @returns {boolean} 是否有效
 */
function validateFileSize(file, maxSize = 5 * 1024 * 1024) { // 默认5MB
    if (!file) return false;
    return file.size <= maxSize;
}

/**
 * 显示验证错误消息
 * @param {string[]} errors - 错误消息数组
 */
function showValidationErrors(errors) {
    if (errors && errors.length > 0) {
        ELEMENT.Message.error(errors.join('；'));
    }
}