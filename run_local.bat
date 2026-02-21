@echo off
REM 在仓库根目录运行：创建 venv（若不存在）、安装依赖、启动 demo 服务
cd /d "%~dp0"

if not exist "venv" (
    echo Creating venv...
    python -m venv venv
)
call venv\Scripts\activate
pip install -q -r requirements.txt
python demo_project/manage.py runserver
