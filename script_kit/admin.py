from django.contrib import admin
from .models import ScriptDefinition, ScriptExecution, ScriptParameterPreset


@admin.register(ScriptDefinition)
class ScriptDefinitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'script_file', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description', 'category']
    fieldsets = (
        (None, {'fields': ('name', 'description', 'category', 'script_file', 'parameters', 'default_parameters')}),
        ('时间', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ScriptExecution)
class ScriptExecutionAdmin(admin.ModelAdmin):
    list_display = ['script', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'script__category']
    readonly_fields = ['script', 'status', 'parameters_used', 'result', 'error_message', 'created_at', 'completed_at', 'duration']


@admin.register(ScriptParameterPreset)
class ScriptParameterPresetAdmin(admin.ModelAdmin):
    list_display = ['name', 'script', 'updated_at']
    list_filter = ['script__category']
    search_fields = ['name', 'script__name']
