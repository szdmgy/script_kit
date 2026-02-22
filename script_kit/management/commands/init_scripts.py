"""初始化测试用 ScriptDefinition（幂等：已存在则跳过）"""
from django.core.management.base import BaseCommand
from script_kit.models import ScriptDefinition


INITIAL_SCRIPTS = [
    {
        'name': '列出目录文件',
        'category': 'file_operations',
        'script_file': 'file_operations.list_files',
        'description': '列出指定目录下的文件与子目录',
        'parameters': {
            'directory': {'type': 'text', 'required': True, 'default': '.', 'description': '要列出的目录路径'},
            'pattern': {'type': 'text', 'required': False, 'default': '', 'description': '文件名过滤（包含匹配）'},
        },
        'default_parameters': {'directory': '.', 'pattern': ''},
    },
    {
        'name': '文件详情',
        'category': 'file_operations',
        'script_file': 'file_operations.file_info',
        'description': '获取指定文件的大小、创建/修改时间等信息',
        'parameters': {
            'filepath': {'type': 'text', 'required': True, 'default': '', 'description': '文件路径'},
        },
        'default_parameters': {'filepath': ''},
    },
    {
        'name': '合并 JSON 文件',
        'category': 'data_processing',
        'script_file': 'data_processing.merge_json',
        'description': '将目录下多个 JSON 文件合并为一个（支持试运行）',
        'parameters': {
            'input_dir': {'type': 'text', 'required': True, 'default': '.', 'description': '包含 JSON 文件的目录'},
            'output_file': {'type': 'text', 'required': True, 'default': 'merged.json', 'description': '输出文件路径'},
        },
        'default_parameters': {'input_dir': '.', 'output_file': 'merged.json'},
    },
    {
        'name': 'CSV 统计摘要',
        'category': 'data_processing',
        'script_file': 'data_processing.csv_summary',
        'description': '读取 CSV 文件，返回行列数、数值列统计（min/max/avg）及前 5 行预览',
        'parameters': {
            'filepath': {'type': 'text', 'required': True, 'default': '', 'description': 'CSV 文件路径'},
            'encoding': {'type': 'text', 'required': False, 'default': 'utf-8', 'description': '文件编码'},
        },
        'default_parameters': {'filepath': '', 'encoding': 'utf-8'},
    },
]


class Command(BaseCommand):
    help = '初始化 script_kit 测试用脚本定义（幂等）'

    def handle(self, *args, **options):
        created_count = 0
        for item in INITIAL_SCRIPTS:
            obj, created = ScriptDefinition.objects.get_or_create(
                name=item['name'],
                defaults=item,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  创建: {obj.name}'))
            else:
                self.stdout.write(f'  已存在: {obj.name}')
        self.stdout.write(self.style.SUCCESS(f'完成，新建 {created_count} 条。'))
