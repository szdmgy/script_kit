"""获取指定文件的详细信息"""
import os
import time


def main(params):
    filepath = params.get('filepath', '')

    if not filepath:
        return {'status': 'error', 'message': '请提供 filepath 参数'}

    if not os.path.exists(filepath):
        return {'status': 'error', 'message': f'文件不存在: {filepath}'}

    stat = os.stat(filepath)
    return {
        'status': 'success',
        'message': f'文件信息获取成功',
        'filepath': os.path.abspath(filepath),
        'name': os.path.basename(filepath),
        'is_file': os.path.isfile(filepath),
        'is_dir': os.path.isdir(filepath),
        'size_bytes': stat.st_size,
        'created': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_ctime)),
        'modified': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
    }
