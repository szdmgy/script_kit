# script_kit 配置：从 Django settings 读取，未配置时使用默认值
from django.conf import settings

DEFAULT_SCRIPTS_ROOT = 'script_kit.scripts'


def get_scripts_root():
    """脚本根包路径，用于动态 import 与扫描。从 settings.SCRIPT_KIT_SCRIPTS_ROOT 读取，未配置时默认 script_kit.scripts。"""
    return getattr(settings, 'SCRIPT_KIT_SCRIPTS_ROOT', DEFAULT_SCRIPTS_ROOT)
