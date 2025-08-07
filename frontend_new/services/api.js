// API基础服务

// API基础配置
const API_BASE_URL = 'http://localhost:5000/api';

// 创建axios实例
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器
apiClient.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么
        console.log('API Request:', config.method?.toUpperCase(), config.url);
        return config;
    },
    error => {
        // 对请求错误做些什么
        console.error('Request Error:', error);
        return Promise.reject(error);
    }
);

// 响应拦截器
apiClient.interceptors.response.use(
    response => {
        // 对响应数据做点什么
        console.log('API Response:', response.status, response.config.url);
        return response;
    },
    error => {
        // 对响应错误做点什么
        console.error('Response Error:', error.response?.status, error.response?.data);
        
        // 统一错误处理
        const message = error.response?.data?.message || error.message || '网络错误';
        
        // 显示错误消息
        if (typeof ELEMENT !== 'undefined') {
            ELEMENT.Message.error(message);
        } else {
            alert(message);
        }
        
        return Promise.reject(error);
    }
);

// API方法封装
const API = {
    // GET请求
    get: (url, params = {}) => {
        return apiClient.get(url, { params });
    },
    
    // POST请求
    post: (url, data = {}) => {
        return apiClient.post(url, data);
    },
    
    // PUT请求
    put: (url, data = {}) => {
        return apiClient.put(url, data);
    },
    
    // DELETE请求
    delete: (url) => {
        return apiClient.delete(url);
    },
    
    // 文件下载
    download: (url, params = {}) => {
        return apiClient.get(url, {
            params,
            responseType: 'blob'
        });
    },
    
    // 文件上传
    upload: (url, formData) => {
        return apiClient.post(url, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    }
};

// 导出API实例
window.API = API;