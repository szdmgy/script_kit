from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


def script_kit_view(request):
    """执行页 - 阶段 1 先用空数据，阶段 2 迁移后再从模型取数"""
    try:
        from .models import ScriptDefinition
        scripts = ScriptDefinition.objects.all().order_by('category', 'name')
        categories = list(
            ScriptDefinition.objects.values_list('category', flat=True).distinct().order_by('category')
        )
    except Exception:
        scripts = []
        categories = []
    return render(request, 'script_kit/index.html', {
        'scripts': scripts,
        'categories': categories,
    })


@staff_member_required
def manage_scripts_view(request):
    """管理页"""
    return render(request, 'script_kit/manage.html', {'page': 'manage'})
