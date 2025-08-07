@echo off
chcp 65001
echo 正在启动华巡网络设备巡检系统（重构版）...

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请确保已安装Python并添加到系统环境变量中
    pause
    exit /b 1
)

REM 删除旧的数据库文件（首次运行时）
REM if exist network_inspection.db (
REM     echo 正在删除旧的数据库文件...
REM     del network_inspection.db
REM )

REM 安装依赖（首次运行时）
REM echo 正在安装依赖...
REM pip install -r requirements.txt
REM if errorlevel 1 (
REM     echo 错误：依赖安装失败，请检查网络连接或手动运行 pip install -r requirements.txt
REM     pause
REM     exit /b 1
REM )

REM 设置环境变量
set FLASK_ENV=development
set PYTHONPATH=%PYTHONPATH%;%cd%

REM 启动后端服务（重构版）
echo 正在启动后端服务（重构版）...
start python app_new.py

REM 等待后端服务启动
echo 等待后端服务启动...
timeout /t 5

REM 检查后端服务是否正常运行
curl http://localhost:5000/api/devices >nul 2>&1
if errorlevel 1 (
    echo 错误：后端服务启动失败
    echo 请检查：
    echo 1. 端口5000是否被占用
    echo 2. 查看命令行窗口中的错误信息
    echo 3. 确保所有依赖都已正确安装
    echo 4. 检查Python路径设置
    pause
    exit /b 1
)

REM 启动前端页面（重构版）
echo 正在启动前端页面（重构版）...
start frontend_new/index.html

echo 系统已启动！
echo 后端服务运行在 http://localhost:5000
echo 前端页面已打开（重构版）
echo.
echo 重构版特性：
echo - 模块化的后端架构（MVC模式）
echo - 分层的前端代码结构
echo - 更好的代码可维护性
echo - 统一的错误处理和日志记录
echo.
echo 注意：首次运行后，请将上方注释的数据库清理和依赖安装命令取消注释