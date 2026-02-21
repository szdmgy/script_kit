# script_kit — 脚本管理与执行标准件

Django App 形态的脚本管理 + 执行标准件，供各业务项目复用。详见 `开发计划.md`、`脚本管理与执行标准件-需求说明书.md`。

---

## 环境依赖（推荐：项目内 venv，勿用全局 Python）

**不要**在系统全局安装依赖，请在本项目下使用**虚拟环境**：

```bash
# 在仓库根目录 G:\cursor\projects\script_kit 下执行
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS
pip install -r requirements.txt
```

之后运行、迁移等都在**已激活的 venv** 下执行，例如：

```bash
python demo_project/manage.py migrate
python demo_project/manage.py runserver
```

`.gitignore` 已排除 `venv/`，不会把虚拟环境提交到仓库。

---

## 提交与推送到 GitHub

### 最简单：一键批处理（推荐）

在项目根目录**双击运行 `push.bat`** 即可：自动 `git add .`、提交、推送到 GitHub。

- 使用默认提交说明：直接双击 `push.bat`。
- 自定义提交说明：在资源管理器中按住 Shift 右键「在此处打开 PowerShell 窗口」，执行：  
  `.\push.bat "feat: 阶段 3 完成"`

首次使用前请确保已执行过：
```bash
git remote add origin https://github.com/szdmgy/script-kit.git
```
（若已添加过可跳过。）

### 或用 Cursor 图形界面

1. 左侧点 **源代码管理（Ctrl+Shift+G）**
2. 勾选要提交的文件，填写提交说明，点 **✓ 提交**
3. 点 **⋯** → **推送**，或顶部 **同步更改**

### 让 Cursor 助手代你执行 git（可选）

若希望对话中的助手能直接执行 `git push` 等命令，需本机终端能访问 Git 和网络：

- 在 Cursor 里用 **终端** 打开项目目录（`G:\cursor\projects\script_kit`），确认能执行 `git status`、`git push` 且不报错。
- 若使用 GitHub HTTPS，首次 push 时按提示在浏览器或弹窗中登录 GitHub 即可；之后会记住凭据。
- 若助手在「代理/沙箱」环境下运行，可能无法执行你本机的 git，此时用上面的 **push.bat** 或 **源代码管理** 即可。

建议每完成一个阶段或每日收工时推送一次；提交前检查不要包含敏感信息（密码、API Key 等）。

---

## 快速运行

| 方式 | 说明 |
|------|------|
| **本地（推荐 venv）** | 如上创建并激活 venv，`pip install -r requirements.txt`，再 `python demo_project/manage.py runserver` |
| **Docker** | 仓库根目录执行 `docker-compose up`，访问 http://localhost:8000/script-kit/ |
