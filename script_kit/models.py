from django.db import models
from django.utils.translation import gettext_lazy as _


class ScriptDefinition(models.Model):
    """脚本定义"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("脚本名称"),
        help_text=_("脚本的唯一标识名称"),
    )
    description = models.TextField(
        verbose_name=_("描述"),
        help_text=_("脚本功能的详细说明"),
        blank=True,
        null=True,
    )
    category = models.CharField(
        max_length=50,
        verbose_name=_("脚本分类"),
        help_text=_("脚本所属的分类，如：file_operations, data_processing 等"),
    )
    script_file = models.CharField(
        max_length=200,
        verbose_name=_("脚本文件"),
        help_text=_("对应的 Python 脚本路径，如：file_operations.merge_json"),
    )
    parameters = models.JSONField(
        default=dict,
        verbose_name=_("参数配置"),
        help_text=_("脚本参数配置，JSON 格式：param_name -> type/required/default/description"),
    )
    default_parameters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("缺省参数"),
        help_text=_("执行页打开时用于填充表单的默认参数键值对"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = _("脚本定义")
        verbose_name_plural = _("脚本定义")
        ordering = ['-created_at']
        db_table = 'script_kit_definition'

    def __str__(self):
        return f"{self.name} ({self.category}/{self.script_file})"


class ScriptExecution(models.Model):
    """脚本执行记录"""
    STATUS_CHOICES = [
        ('pending', _('等待中')),
        ('running', _('运行中')),
        ('completed', _('已完成')),
        ('failed', _('失败')),
        ('cancelled', _('已取消')),
    ]

    script = models.ForeignKey(
        ScriptDefinition,
        on_delete=models.CASCADE,
        verbose_name=_("关联脚本"),
        help_text=_("执行的脚本定义"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("状态"),
    )
    parameters_used = models.JSONField(default=dict, verbose_name=_("使用参数"))
    result = models.JSONField(default=dict, verbose_name=_("执行结果"))
    error_message = models.TextField(blank=True, null=True, verbose_name=_("错误信息"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("完成时间"))
    duration = models.FloatField(default=0.0, verbose_name=_("执行时长(秒)"))

    class Meta:
        verbose_name = _("脚本执行记录")
        verbose_name_plural = _("脚本执行记录")
        ordering = ['-created_at']
        db_table = 'script_kit_execution'

    def __str__(self):
        return f"{self.script.name} - {self.get_status_display()}"


class ScriptParameterPreset(models.Model):
    """参数预设：为某脚本保存的常用参数组合"""
    script = models.ForeignKey(
        ScriptDefinition,
        on_delete=models.CASCADE,
        related_name='parameter_presets',
        verbose_name=_("关联脚本"),
    )
    name = models.CharField(max_length=100, verbose_name=_("预设名称"))
    parameters = models.JSONField(default=dict, verbose_name=_("参数键值对"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))

    class Meta:
        verbose_name = _("参数预设")
        verbose_name_plural = _("参数预设")
        db_table = 'script_kit_parameter_preset'
        constraints = [
            models.UniqueConstraint(fields=['script', 'name'], name='script_kit_preset_script_name_unique'),
        ]

    def __str__(self):
        return f"{self.script.name} — {self.name}"
