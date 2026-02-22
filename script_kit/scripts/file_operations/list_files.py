"""列出指定目录下的文件列表"""
import os


def main(params):
    directory = params.get('directory', '.')
    pattern = params.get('pattern', '')

    if not os.path.isdir(directory):
        return {'status': 'error', 'message': f'目录不存在: {directory}'}

    files = []
    for name in sorted(os.listdir(directory)):
        full = os.path.join(directory, name)
        if pattern and pattern not in name:
            continue
        files.append({
            'name': name,
            'is_dir': os.path.isdir(full),
            'size': os.path.getsize(full) if os.path.isfile(full) else None,
        })

    return {
        'status': 'success',
        'message': f'找到 {len(files)} 个条目',
        'directory': os.path.abspath(directory),
        'count': len(files),
        'files': files,
    }
