# 基于配置化 root 的脚本执行：import 与 main(params) 调用
import importlib

from .conf import get_scripts_root


def run_script(script_def, params):
    """
    根据 script_def.script_file 从配置的脚本根路径动态导入并调用 main(params)。
    script_file 格式：category.module_name，如 file_operations.merge_json。
    返回 main() 的返回值（dict）；若导入或执行异常则抛出。
    """
    root = get_scripts_root()
    module_path = f'{root}.{script_def.script_file}'
    mod = importlib.import_module(module_path)
    main = getattr(mod, 'main', None)
    if main is None:
        raise AttributeError(f'脚本模块 {module_path} 未提供 main(params) 函数')
    return main(params)
