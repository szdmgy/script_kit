# Generated for script_kit (stage 2)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ScriptDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='脚本的唯一标识名称', max_length=100, unique=True, verbose_name='脚本名称')),
                ('description', models.TextField(blank=True, help_text='脚本功能的详细说明', null=True, verbose_name='描述')),
                ('category', models.CharField(help_text='脚本所属的分类，如：file_operations, data_processing 等', max_length=50, verbose_name='脚本分类')),
                ('script_file', models.CharField(help_text='对应的 Python 脚本路径，如：file_operations.merge_json', max_length=200, verbose_name='脚本文件')),
                ('parameters', models.JSONField(default=dict, help_text='脚本参数配置，JSON 格式：param_name -> type/required/default/description', verbose_name='参数配置')),
                ('default_parameters', models.JSONField(blank=True, default=dict, help_text='执行页打开时用于填充表单的默认参数键值对', verbose_name='缺省参数')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '脚本定义',
                'verbose_name_plural': '脚本定义',
                'db_table': 'script_kit_definition',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ScriptExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', '等待中'), ('running', '运行中'), ('completed', '已完成'), ('failed', '失败'), ('cancelled', '已取消')], default='pending', max_length=20, verbose_name='状态')),
                ('parameters_used', models.JSONField(default=dict, verbose_name='使用参数')),
                ('result', models.JSONField(default=dict, verbose_name='执行结果')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='错误信息')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='完成时间')),
                ('duration', models.FloatField(default=0.0, verbose_name='执行时长(秒)')),
                ('script', models.ForeignKey(help_text='执行的脚本定义', on_delete=django.db.models.deletion.CASCADE, to='script_kit.scriptdefinition', verbose_name='关联脚本')),
            ],
            options={
                'verbose_name': '脚本执行记录',
                'verbose_name_plural': '脚本执行记录',
                'db_table': 'script_kit_execution',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ScriptParameterPreset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='预设名称')),
                ('parameters', models.JSONField(default=dict, verbose_name='参数键值对')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameter_presets', to='script_kit.scriptdefinition', verbose_name='关联脚本')),
            ],
            options={
                'verbose_name': '参数预设',
                'verbose_name_plural': '参数预设',
                'db_table': 'script_kit_parameter_preset',
            },
        ),
        migrations.AddConstraint(
            model_name='scriptparameterpreset',
            constraint=models.UniqueConstraint(name='script_kit_preset_script_name_unique', fields=('script', 'name')),
        ),
    ]
