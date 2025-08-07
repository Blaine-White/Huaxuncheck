// 日期时间工具函数

/**
 * 格式化日期时间
 * @param {string|Date} datetime - 日期时间
 * @returns {string} 格式化后的日期时间字符串
 */
function formatDateTime(datetime) {
    if (!datetime) return '';
    
    const date = new Date(datetime);
    if (isNaN(date.getTime())) return '';
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * 获取当前日期时间字符串
 * @returns {string} 当前日期时间
 */
function getCurrentDateTime() {
    const now = new Date();
    return formatDateTime(now);
}

/**
 * 获取星期几
 * @returns {string} 星期几
 */
function getWeekDay() {
    const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const now = new Date();
    return weekDays[now.getDay()];
}

/**
 * 获取农历信息（简化版）
 * @returns {string} 农历信息
 */
function getLunarInfo() {
    // 简化的农历信息，实际项目中可以使用专门的农历库
    const now = new Date();
    const month = now.getMonth() + 1;
    const day = now.getDate();
    
    // 简单的节气和节日判断
    const festivals = {
        '1-1': '元旦',
        '2-14': '情人节',
        '3-8': '妇女节',
        '5-1': '劳动节',
        '6-1': '儿童节',
        '10-1': '国庆节',
        '12-25': '圣诞节'
    };
    
    const key = `${month}-${day}`;
    return festivals[key] || `农历${month}月${day}日`;
}

/**
 * 计算时间差
 * @param {string|Date} startTime - 开始时间
 * @param {string|Date} endTime - 结束时间
 * @returns {string} 时间差描述
 */
function getTimeDifference(startTime, endTime = new Date()) {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const diff = end - start;
    
    if (diff < 0) return '时间错误';
    
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}天前`;
    if (hours > 0) return `${hours}小时前`;
    if (minutes > 0) return `${minutes}分钟前`;
    return `${seconds}秒前`;
}

/**
 * 格式化持续时间（秒）
 * @param {number} seconds - 秒数
 * @returns {string} 格式化的持续时间
 */
function formatDuration(seconds) {
    if (!seconds || seconds <= 0) return '—';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    
    let result = '';
    if (hours > 0) result += `${hours}小时`;
    if (minutes > 0) result += `${minutes}分钟`;
    if (remainingSeconds > 0 || result === '') result += `${remainingSeconds}秒`;
    
    return result;
}