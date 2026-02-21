#!/usr/bin/env python
"""Django's command-line utility for demo_project."""
import os
import sys
from pathlib import Path

# 将 script_kit 仓库根目录加入 path，以便 import script_kit
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)
