"""
script_kit 一键配置脚本 — 自动将 script_kit 接入当前 Django 项目。

使用方式：
  复制方式：python script_kit/setup_project.py
  pip 方式：python -m script_kit.setup_project
"""
import os
import re
import sys
import shutil
import subprocess


def find_manage_py():
    """从当前目录向上查找 manage.py"""
    d = os.getcwd()
    for _ in range(5):
        if os.path.isfile(os.path.join(d, 'manage.py')):
            return d
        d = os.path.dirname(d)
    return None


def get_project_name(project_root):
    """从 manage.py 中提取 DJANGO_SETTINGS_MODULE 对应的项目名"""
    manage_path = os.path.join(project_root, 'manage.py')
    with open(manage_path, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r"['\"](\w+)\.settings['\"]", content)
    return m.group(1) if m else None


def backup_file(filepath):
    bak = filepath + '.bak'
    shutil.copy2(filepath, bak)
    print(f'  备份: {bak}')


def setup_settings(settings_path):
    """在 settings.py 中添加 script_kit 相关配置"""
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    if "'script_kit'" not in content and '"script_kit"' not in content:
        content = re.sub(
            r"(INSTALLED_APPS\s*=\s*\[)(.*?)(])",
            lambda m: m.group(1) + m.group(2).rstrip() +
            ("\n    " if not m.group(2).rstrip().endswith(',') else "\n    ") +
            "'script_kit',\n" + m.group(3),
            content,
            count=1,
            flags=re.DOTALL,
        )
        modified = True
        print('  settings.py: 已添加 script_kit 到 INSTALLED_APPS')
    else:
        print('  settings.py: INSTALLED_APPS 已包含 script_kit，跳过')

    if 'SCRIPT_KIT_SCRIPTS_ROOT' not in content:
        content += "\n\n# script_kit 配置：脚本根目录（包路径）\nSCRIPT_KIT_SCRIPTS_ROOT = 'script_kit.scripts'\n"
        modified = True
        print('  settings.py: 已添加 SCRIPT_KIT_SCRIPTS_ROOT')
    else:
        print('  settings.py: SCRIPT_KIT_SCRIPTS_ROOT 已存在，跳过')

    if modified:
        backup_file(settings_path)
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return modified


def setup_urls(urls_path):
    """在 urls.py 中添加 script_kit URL 挂载"""
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'script_kit.urls' in content:
        print('  urls.py: script_kit.urls 已挂载，跳过')
        return False

    import_lines = [l for l in content.splitlines() if l.startswith('from django.urls') or l.startswith('import ')]
    has_include_import = any('include' in l for l in import_lines)
    if not has_include_import:
        content = content.replace(
            'from django.urls import path',
            'from django.urls import path, include',
        )

    content = re.sub(
        r"(urlpatterns\s*=\s*\[)",
        r"\1\n    path('script-kit/', include('script_kit.urls')),",
        content,
        count=1,
    )

    backup_file(urls_path)
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('  urls.py: 已添加 script-kit/ 路由')
    return True


def run_migrate(project_root):
    """执行 migrate"""
    manage_py = os.path.join(project_root, 'manage.py')
    print('  执行 migrate...')
    result = subprocess.run(
        [sys.executable, manage_py, 'migrate', '--no-color'],
        cwd=project_root,
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        has_new = 'Applying script_kit' in result.stdout
        if has_new:
            print('  migrate: script_kit 表已创建')
        else:
            print('  migrate: 表已存在，无新迁移')
    else:
        print(f'  migrate 失败: {result.stderr[:200]}')


def main():
    print('=== script_kit 一键配置 ===\n')

    project_root = find_manage_py()
    if not project_root:
        print('错误: 未找到 manage.py，请在 Django 项目目录下运行此脚本。')
        sys.exit(1)
    print(f'项目根目录: {project_root}')

    project_name = get_project_name(project_root)
    if not project_name:
        print('错误: 无法从 manage.py 中提取项目名，请检查 manage.py 格式。')
        sys.exit(1)
    print(f'项目名称: {project_name}\n')

    settings_path = os.path.join(project_root, project_name, 'settings.py')
    urls_path = os.path.join(project_root, project_name, 'urls.py')

    if not os.path.isfile(settings_path):
        print(f'错误: 未找到 {settings_path}')
        sys.exit(1)
    if not os.path.isfile(urls_path):
        print(f'错误: 未找到 {urls_path}')
        sys.exit(1)

    print('[1/3] 配置 settings.py')
    setup_settings(settings_path)

    print('\n[2/3] 配置 urls.py')
    setup_urls(urls_path)

    print('\n[3/3] 数据库迁移')
    run_migrate(project_root)

    print('\n=== 配置完成 ===')
    print(f'启动服务后访问: http://127.0.0.1:8000/script-kit/')


if __name__ == '__main__':
    main()
