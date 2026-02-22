# script_kit 接入指南

将 script_kit 标准件集成到你的 Django 项目中。

---

## 方式一：一键配置（推荐）

### 复制方式

1. 把 `script_kit/` 整个文件夹复制到新项目根目录（与 `manage.py` 同级）
2. 运行：`python script_kit/setup_project.py`
3. 完成

### pip 方式

1. 安装：`pip install git+https://github.com/szdmgy/script_kit.git`
2. 运行：`python -m script_kit.setup_project`
3. 完成

一键配置脚本会自动完成以下所有步骤：settings.py 注册 app 和配置、urls.py 挂载路由、数据库建表。已配好的不会重复修改，修改前自动备份。

---

## 方式二：手动配置

如果你想手动控制，按以下步骤操作：

### 1. 获取 script_kit

- **复制**：将 `script_kit/` 目录复制到项目中（与 `manage.py` 同级）
- **pip**：`pip install git+https://github.com/szdmgy/script_kit.git`

### 2. settings.py 配置

```python
INSTALLED_APPS = [
    # ... 你的其它 app ...
    'script_kit',
]

# 脚本根目录（包路径），指向你放脚本的 Python 包
# 默认值为 'script_kit.scripts'，若你的脚本放在别处请修改
SCRIPT_KIT_SCRIPTS_ROOT = 'script_kit.scripts'
```

### 3. URL 挂载

在项目的 `urls.py` 中：

```python
from django.urls import path, include

urlpatterns = [
    # ... 你的其它 url ...
    path('script-kit/', include('script_kit.urls')),
]
```

### 4. 执行迁移

```bash
python manage.py migrate
```

会创建三张表：`script_kit_definition`、`script_kit_execution`、`script_kit_parameter_preset`。

### 5.（可选）初始化测试数据

```bash
python manage.py init_scripts
```

幂等命令，会创建 4 条示例脚本定义（file_operations × 2、data_processing × 2）。

---

配置完成后可访问：
- `/script-kit/` — 执行页
- `/script-kit/manage/` — 管理页（需 staff 权限）
- `/script-kit/api/...` — 全部 API

---

## 脚本目录结构

脚本放在 `SCRIPT_KIT_SCRIPTS_ROOT` 指向的包下，按分类建子包：

```
script_kit/scripts/          ← 脚本根包
├── __init__.py
├── file_operations/         ← 分类（子包）
│   ├── __init__.py
│   ├── list_files.py        ← 脚本模块
│   └── file_info.py
└── data_processing/
    ├── __init__.py
    ├── merge_json.py
    └── csv_summary.py
```

- **分类** = 子包名（如 `file_operations`）
- **脚本文件** = 分类下的 `.py` 模块（如 `list_files`）
- ScriptDefinition 中的 `script_file` 字段格式：`category.module_name`（如 `file_operations.list_files`）

## 脚本编写约定

每个脚本模块必须提供 `main(params)` 函数：

```python
def main(params: dict) -> dict:
    """
    params: 前端传入的参数字典
    返回: dict，至少包含 status ('success'/'error') 和 message
    """
    # 你的逻辑
    return {
        'status': 'success',
        'message': '执行完成',
        # ... 其它返回数据
    }
```

### dry_run 支持

涉及数据库写入或文件修改的脚本，建议支持 `dry_run`：

```python
def main(params):
    dry_run = params.get('dry_run', False)

    # ... 准备数据 ...

    if dry_run:
        return {
            'status': 'success',
            'dry_run': True,
            'message': f'[试运行] 将影响 {count} 条记录',
        }

    # ... 实际执行 ...
    return {'status': 'success', 'message': f'已处理 {count} 条记录'}
```

执行框架不解析 `dry_run`，只透传 `params`，由脚本自行判断。

---

## API 清单

所有 API 在 URL 挂载前缀下的 `api/` 路径（如 `/script-kit/api/...`）。

| 路径 | 方法 | 说明 |
|------|------|------|
| `api/scripts/` | GET | 脚本列表 |
| `api/scripts/` | POST | 创建脚本 |
| `api/script/<id>/` | GET / PUT / DELETE | 脚本详情 / 更新 / 删除 |
| `api/scripts-list/` | GET | 精简列表（id / name / category） |
| `api/execute/` | POST | 执行脚本（body: `{script_id, params}`） |
| `api/execution/<id>/` | GET | 执行记录详情 |
| `api/script/<id>/default-parameters/` | GET / PUT | 缺省参数 |
| `api/script/<id>/presets/` | GET / POST | 参数预设列表 / 创建 |
| `api/script/<id>/presets/<pid>/` | GET / PUT / DELETE | 预设详情 / 更新 / 删除 |
| `api/categories/` | GET | 分类列表（从 DB 已有脚本） |
| `api/categories-available/` | GET | 可用分类（扫描文件系统） |
| `api/script-files/<category>/` | GET | 分类下可用脚本文件 |
| `api/import-scripts/` | POST | 批量导入脚本定义（JSON 数组） |
| `api/export-scripts/` | GET | 导出所有脚本定义 |
| `api/execute-by-description/` | POST | 预留（501） |
| `api/query-by-description/` | POST | 预留（501） |

---

## 本地运行

**环境约定：禁止使用全局 Python，须在项目 venv 或 Docker 内运行。**

### venv 方式

```bash
# 仓库根目录下
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python demo_project/manage.py migrate
python demo_project/manage.py init_scripts   # 可选
python demo_project/manage.py runserver
```

或直接双击 `run_local.bat`（自动创建 venv、安装依赖、启动）。

### Docker 方式

```bash
docker-compose up
```

访问 http://localhost:8000/script-kit/。
