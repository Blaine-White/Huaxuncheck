// 华巡网络设备巡检系统 - 主应用

// Vue应用实例
new Vue({
    el: '#app',
    data: {
        // 设备数据
        devices: [],
        inspectionRecords: [],
        selectedDevices: [],
        selectedGroupDevices: [],
        selectedRecords: [],
        
        // 对话框状态
        addDeviceDialogVisible: false,
        editDeviceDialogVisible: false,
        resultDialogVisible: false,
        groupManagerDialogVisible: false,
        importDialogVisible: false,
        inspectionLogDialogVisible: false,
        logDetailsDialogVisible: false,
        
        // 表单数据
        newDevice: {
            name: '',
            ip: '',
            username: '',
            password: '',
            enable_password: '',
            device_type: 'cisco_ios',
            protocol: 'ssh',
            commands: 'show version,show interfaces status,show running-config',
            group: '交换机'
        },
        editingDevice: {
            id: null,
            name: '',
            ip: '',
            username: '',
            password: '',
            enable_password: '',
            device_type: 'cisco_ios',
            protocol: 'ssh',
            commands: '',
            group: '交换机'
        },
        
        // 表单验证规则
        rules: {
            name: [
                { required: true, message: '请输入设备名称', trigger: 'blur' }
            ],
            ip: [
                { required: true, message: '请输入IP地址', trigger: 'blur' },
                { pattern: /^(\d{1,3}\.){3}\d{1,3}$/, message: '请输入正确的IP地址格式', trigger: 'blur' }
            ],
            username: [
                { required: true, message: '请输入用户名', trigger: 'blur' }
            ],
            password: [
                { required: true, message: '请输入密码', trigger: 'blur' }
            ],
            device_type: [
                { required: true, message: '请选择设备类型', trigger: 'change' }
            ],
            protocol: [
                { required: true, message: '请选择连接协议', trigger: 'change' }
            ],
            group: [
                { required: true, message: '请选择设备分组', trigger: 'change' }
            ],
            commands: [
                { required: true, message: '请输入巡检命令', trigger: 'blur' }
            ]
        },
        
        // 巡检相关
        formattedResult: null,
        addingDevice: false,
        updatingDevice: false,
        inspectionInProgress: false,
        inspectionProgress: 0,
        currentInspectingDevice: null,
        batchInspecting: false,
        completedInspections: 0,
        totalInspections: 0,
        
        // 分组管理
        activeDeviceGroupTab: 'all',
        deviceGroups: ['交换机', 'AP', 'PC', '路由器'],
        defaultGroups: ['交换机', 'AP', 'PC', '路由器'],
        newGroupName: '',
        groupPages: {},
        
        // 巡检日志
        inspectionLogs: [],
        currentLogDetails: null,
        logCurrentPage: 1,
        logPageSize: 10,
        
        // 分页
        currentPage: 1,
        pageSize: 10,
        recordCurrentPage: 1,
        recordPageSize: 10,
        
        // 时间显示
        currentDateTime: '',
        lunarInfo: '',
        weekDay: '',
        currentYear: new Date().getFullYear(),
        
        // 状态检查
        statusCheckInterval: null,
        pollingTimeout: null
    },
    
    computed: {
        // 分页后的设备列表
        paginatedDevices() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.devices.slice(start, end);
        },
        
        // 分页后的巡检记录
        paginatedRecords() {
            const start = (this.recordCurrentPage - 1) * this.recordPageSize;
            const end = start + this.recordPageSize;
            return this.inspectionRecords.slice(start, end);
        }
    },
    
    methods: {
        // 时间更新
        updateDateTime() {
            this.currentDateTime = getCurrentDateTime();
            this.weekDay = getWeekDay();
            this.lunarInfo = getLunarInfo();
        },
        
        // 格式化日期时间
        formatDateTime(datetime) {
            return formatDateTime(datetime);
        },
        
        // 获取设备列表
        async fetchDevices() {
            try {
                const devices = await DeviceService.getAllDevices();
                
                // 保存已选择的设备ID
                const selectedIds = this.selectedDevices.map(device => device.id);
                this.devices = devices;
                
                // 收集所有设备的分组信息
                const existingGroups = new Set();
                this.devices.forEach(device => {
                    if (device.group) {
                        existingGroups.add(device.group);
                    }
                });
                
                // 更新设备分组列表
                existingGroups.forEach(group => {
                    const normalizedGroup = group.trim();
                    if (normalizedGroup && !this.deviceGroups.some(g => 
                        typeof g === 'string' 
                            ? g.toLowerCase() === normalizedGroup.toLowerCase()
                            : g.originalName.toLowerCase() === normalizedGroup.toLowerCase()
                    )) {
                        this.deviceGroups.push(normalizedGroup);
                    }
                });
                
                // 确保每个分组都有对应的分页状态
                this.deviceGroups.forEach(group => {
                    if (!this.groupPages[group]) {
                        this.$set(this.groupPages, group, 1);
                    }
                });
                
                // 恢复选中状态
                if (selectedIds.length > 0) {
                    this.selectedDevices = this.devices.filter(device => 
                        selectedIds.includes(device.id)
                    );
                }
                
            } catch (error) {
                console.error('获取设备列表失败:', error);
                this.$message.error('获取设备列表失败');
            }
        },
        
        // 获取巡检记录
        async fetchInspectionRecords() {
            try {
                const response = await API.get('/records');
                this.inspectionRecords = response.data.records || response.data;
            } catch (error) {
                console.error('获取巡检记录失败:', error);
                this.$message.error('获取巡检记录失败');
            }
        },
        
        // 显示添加设备对话框
        showAddDeviceDialog() {
            this.newDevice = {
                name: '',
                ip: '',
                username: '',
                password: '',
                enable_password: '',
                device_type: 'cisco_ios',
                protocol: 'ssh',
                commands: 'show version,show interfaces status,show running-config',
                group: '交换机'
            };
            this.addDeviceDialogVisible = true;
        },
        
        // 添加设备
        async addDevice() {
            try {
                await this.$refs.addDeviceForm.validate();
                
                this.addingDevice = true;
                await DeviceService.createDevice(this.newDevice);
                
                this.$message.success('设备添加成功');
                this.addDeviceDialogVisible = false;
                await this.fetchDevices();
                
            } catch (error) {
                if (error.message !== '数据验证失败') {
                    console.error('添加设备失败:', error);
                }
            } finally {
                this.addingDevice = false;
            }
        },
        
        // 编辑设备
        editDevice(device) {
            this.editingDevice = { ...device };
            this.editDeviceDialogVisible = true;
        },
        
        // 更新设备
        async updateDevice() {
            try {
                await this.$refs.editDeviceForm.validate();
                
                this.updatingDevice = true;
                await DeviceService.updateDevice(this.editingDevice.id, this.editingDevice);
                
                this.$message.success('设备更新成功');
                this.editDeviceDialogVisible = false;
                await this.fetchDevices();
                
            } catch (error) {
                if (error.message !== '数据验证失败') {
                    console.error('更新设备失败:', error);
                }
            } finally {
                this.updatingDevice = false;
            }
        },
        
        // 删除设备
        async deleteDevice(deviceId) {
            try {
                await this.$confirm('确定要删除这个设备吗？', '提示', {
                    type: 'warning'
                });
                
                await DeviceService.deleteDevice(deviceId);
                this.$message.success('设备删除成功');
                await this.fetchDevices();
                
            } catch (error) {
                if (error !== 'cancel') {
                    console.error('删除设备失败:', error);
                }
            }
        },
        
        // 导出设备
        async exportDevices() {
            try {
                await DeviceService.exportDevices();
            } catch (error) {
                console.error('导出设备失败:', error);
            }
        },
        
        // 分页处理
        handleDevicePageChange(page) {
            this.currentPage = page;
        },
        
        handleGroupPageChange(group, page) {
            this.$set(this.groupPages, group, page);
        },
        
        handleRecordPageChange(page) {
            this.recordCurrentPage = page;
        },
        
        // 设备选择处理
        handleDeviceSelectionChange(selection) {
            this.selectedDevices = selection;
        },
        
        handleGroupDeviceSelectionChange(selection) {
            this.selectedGroupDevices = selection;
        },
        
        handleRecordSelectionChange(selection) {
            this.selectedRecords = selection;
        },
        
        // 根据分组过滤设备
        filterDevicesByGroup(group) {
            const filtered = this.devices.filter(device => {
                if (!device.group) return false;
                
                const deviceGroupLower = device.group.toLowerCase().trim();
                const targetGroupLower = group.toLowerCase().trim();
                return deviceGroupLower === targetGroupLower;
            });
            
            return filtered;
        },
        
        // 分组设备分页
        paginatedGroupDevices(group) {
            const filtered = this.filterDevicesByGroup(group);
            const page = this.groupPages[group] || 1;
            const start = (page - 1) * this.pageSize;
            const end = start + this.pageSize;
            return filtered.slice(start, end);
        },
        
        // 启动状态检查
        startStatusCheck() {
            // 这里可以添加定期检查设备状态的逻辑
            console.log('设备状态检查已启动');
        },
        
        // 停止状态检查
        stopStatusCheck() {
            if (this.statusCheckInterval) {
                clearInterval(this.statusCheckInterval);
                this.statusCheckInterval = null;
            }
            
            if (this.pollingTimeout) {
                clearTimeout(this.pollingTimeout);
                this.pollingTimeout = null;
            }
        }
    },
    
    mounted() {
        // 初始化时首先更新日期时间
        this.updateDateTime();
        
        // 设置定时器每秒更新一次时间
        setInterval(() => {
            this.updateDateTime();
        }, 1000);
        
        // 获取设备列表和巡检记录
        this.fetchDevices().then(() => {
            this.fetchInspectionRecords();
        });
        
        // 启动设备状态检查
        this.startStatusCheck();
    },
    
    beforeDestroy() {
        // 组件销毁前清除定时器
        this.stopStatusCheck();
    }
});