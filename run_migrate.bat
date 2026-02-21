@echo off
REM 在仓库根目录运行：使用项目 venv 安装依赖并执行 migrate（不启动服务）
cd /d "%~dp0"

if not exist "venv" (
    echo Creating venv...
    python -m venv venv
)
call venv\Scripts\activate
pip install -q -r requirements.txt
python demo_project/manage.py migrate
echo.
echo Migrate 完成。启动服务请运行 run_local.bat 或使用 docker-compose up。
pause
