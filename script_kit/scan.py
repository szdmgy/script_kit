# 基于配置化 root 的脚本扫描：分类与 .py 模块列表
import importlib
import pkgutil

from .conf import get_scripts_root


def get_categories():
    """
    返回脚本根包下的分类列表（子包名），如 ['file_operations', 'data_processing']。
    仅包含作为包（含 __init__.py 或可迭代子模块）的子目录。
    """
    root = get_scripts_root()
    try:
        root_mod = importlib.import_module(root)
    except ImportError:
        return []
    if not hasattr(root_mod, '__path__'):
        return []
    categories = []
    for importer, name, ispkg in pkgutil.iter_modules(root_mod.__path__):
        if ispkg and not name.startswith('_'):
            categories.append(name)
    return sorted(categories)


def get_script_files(category):
    """
    返回指定分类下的脚本模块名列表（不含 .py），如 ['merge_json', 'copy_file']。
    仅包含可直接 import 的模块，排除 __init__。
    """
    root = get_scripts_root()
    try:
        cat_mod = importlib.import_module(f'{root}.{category}')
    except ImportError:
        return []
    if not hasattr(cat_mod, '__path__'):
        return []
    files = []
    for importer, name, ispkg in pkgutil.iter_modules(cat_mod.__path__):
        if not name.startswith('_') and name != '__init__':
            files.append(name)
    return sorted(files)
