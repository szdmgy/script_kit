@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo [1/4] 添加所有变更...
git add .
if errorlevel 1 ( echo 错误: git add 失败 & pause & exit /b 1 )

echo [2/4] 状态...
git status --short

echo [3/4] 提交（若无可提交变更会提示）...
if "%~1"=="" (
    git commit -m "chore: update"
) else (
    git commit -m "%~1"
)
if errorlevel 1 (
    echo 未提交（可能没有变更或已提交过）
) else (
    echo 提交完成
)

echo [4/4] 推送到 GitHub...
git push
if errorlevel 1 (
    echo.
    echo 推送失败。请检查：1）是否已 git remote add origin 你的仓库地址  2）是否已登录 GitHub
    pause
    exit /b 1
)

echo.
echo 推送成功。
pause
