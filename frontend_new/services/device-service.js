// 设备服务

const DeviceService = {
    // 获取所有设备
    async getAllDevices() {
        try {
            const response = await API.get('/devices');
            return response.data;
        } catch (error) {
            console.error('获取设备列表失败:', error);
            throw error;
        }
    },
    
    // 创建设备
    async createDevice(deviceData) {
        try {
            // 前端验证
            const validation = validateDeviceData(deviceData);
            if (!validation.isValid) {
                showValidationErrors(validation.errors);
                throw new Error('数据验证失败');
            }
            
            const response = await API.post('/devices', deviceData);
            return response.data;
        } catch (error) {
            console.error('创建设备失败:', error);
            throw error;
        }
    },
    
    // 更新设备
    async updateDevice(deviceId, deviceData) {
        try {
            // 前端验证
            const validation = validateDeviceData(deviceData);
            if (!validation.isValid) {
                showValidationErrors(validation.errors);
                throw new Error('数据验证失败');
            }
            
            const response = await API.put(`/devices/${deviceId}`, deviceData);
            return response.data;
        } catch (error) {
            console.error('更新设备失败:', error);
            throw error;
        }
    },
    
    // 删除设备
    async deleteDevice(deviceId) {
        try {
            const response = await API.delete(`/devices/${deviceId}`);
            return response.data;
        } catch (error) {
            console.error('删除设备失败:', error);
            throw error;
        }
    },
    
    // 导出设备
    async exportDevices() {
        try {
            const response = await API.download('/devices/export');
            
            // 创建下载链接
            const blob = new Blob([response.data], {
                type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            });
            
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `设备信息_${formatDateTime(new Date()).replace(/[:\s]/g, '_')}.xlsx`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            
            ELEMENT.Message.success('设备信息导出成功');
        } catch (error) {
            console.error('导出设备失败:', error);
            throw error;
        }
    },
    
    // 导入设备
    async importDevices(file) {
        try {
            // 验证文件
            if (!validateFileType(file)) {
                throw new Error('只支持Excel文件格式');
            }
            
            if (!validateFileSize(file)) {
                throw new Error('文件大小不能超过5MB');
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await API.upload('/devices/import', formData);
            return response.data;
        } catch (error) {
            console.error('导入设备失败:', error);
            throw error;
        }
    },
    
    // 获取设备分组
    async getDeviceGroups() {
        try {
            const response = await API.get('/devices/groups');
            return response.data;
        } catch (error) {
            console.error('获取设备分组失败:', error);
            throw error;
        }
    },
    
    // 根据分组获取设备
    async getDevicesByGroup(groupName) {
        try {
            const response = await API.get(`/devices/groups/${encodeURIComponent(groupName)}`);
            return response.data;
        } catch (error) {
            console.error('获取分组设备失败:', error);
            throw error;
        }
    }
};

// 导出设备服务
window.DeviceService = DeviceService;