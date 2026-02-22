"""
script_kit 后端 API — 纯 Django JsonResponse 实现，无需 DRF。
所有 API 挂载在 script-kit/api/ 前缀下。
"""
import json
import traceback
from datetime import timezone as tz

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404

from .models import ScriptDefinition, ScriptExecution, ScriptParameterPreset
from .conf import get_scripts_root
from .runner import run_script
from .scan import get_categories as scan_categories, get_script_files


def _parse_json_body(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return None


def _script_to_dict(s):
    return {
        'id': s.id,
        'name': s.name,
        'description': s.description or '',
        'category': s.category,
        'script_file': s.script_file,
        'parameters': s.parameters,
        'default_parameters': s.default_parameters,
        'created_at': s.created_at.isoformat() if s.created_at else None,
        'updated_at': s.updated_at.isoformat() if s.updated_at else None,
    }


def _execution_to_dict(e):
    return {
        'id': e.id,
        'script_id': e.script_id,
        'script_name': e.script.name,
        'status': e.status,
        'parameters_used': e.parameters_used,
        'result': e.result,
        'error_message': e.error_message or '',
        'created_at': e.created_at.isoformat() if e.created_at else None,
        'completed_at': e.completed_at.isoformat() if e.completed_at else None,
        'duration': e.duration,
    }


def _preset_to_dict(p):
    return {
        'id': p.id,
        'script_id': p.script_id,
        'name': p.name,
        'parameters': p.parameters,
        'created_at': p.created_at.isoformat() if p.created_at else None,
        'updated_at': p.updated_at.isoformat() if p.updated_at else None,
    }


# ── Scripts CRUD ─────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def scripts_list_create(request):
    """GET: 脚本列表；POST: 创建脚本"""
    if request.method == 'GET':
        qs = ScriptDefinition.objects.all().order_by('category', 'name')
        return JsonResponse([_script_to_dict(s) for s in qs], safe=False)

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({'error': '请求体必须为有效 JSON'}, status=400)
    required = ('name', 'category', 'script_file')
    missing = [f for f in required if not data.get(f)]
    if missing:
        return JsonResponse({'error': f'缺少必填字段: {", ".join(missing)}'}, status=400)
    try:
        s = ScriptDefinition.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            category=data['category'],
            script_file=data['script_file'],
            parameters=data.get('parameters', {}),
            default_parameters=data.get('default_parameters', {}),
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse(_script_to_dict(s), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def script_detail(request, script_id):
    """GET: 脚本详情；PUT: 更新；DELETE: 删除"""
    s = get_object_or_404(ScriptDefinition, pk=script_id)
    if request.method == 'GET':
        return JsonResponse(_script_to_dict(s))

    if request.method == 'DELETE':
        s.delete()
        return JsonResponse({'ok': True})

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({'error': '请求体必须为有效 JSON'}, status=400)
    for field in ('name', 'description', 'category', 'script_file', 'parameters', 'default_parameters'):
        if field in data:
            setattr(s, field, data[field])
    s.save()
    return JsonResponse(_script_to_dict(s))


@require_GET
def scripts_simple_list(request):
    """精简列表：仅返回 id/name/category（供下拉选择等场景）"""
    qs = ScriptDefinition.objects.all().order_by('category', 'name')
    return JsonResponse([
        {'id': s.id, 'name': s.name, 'category': s.category}
        for s in qs
    ], safe=False)


# ── Execution ────────────────────────────────────────────

@require_GET
def execution_detail(request, execution_id):
    """执行记录详情"""
    e = get_object_or_404(ScriptExecution, pk=execution_id)
    return JsonResponse(_execution_to_dict(e))


# ── Execute ──────────────────────────────────────────────

@csrf_exempt
@require_POST
def execute_script(request):
    """执行脚本：body 需含 script_id、params（可含 dry_run）"""
    from django.utils import timezone as django_tz

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({'error': '请求体必须为有效 JSON'}, status=400)
    script_id = data.get('script_id')
    if not script_id:
        return JsonResponse({'error': '缺少 script_id'}, status=400)
    s = get_object_or_404(ScriptDefinition, pk=script_id)
    params = data.get('params', {})

    execution = ScriptExecution.objects.create(script=s, status='running', parameters_used=params)
    start = django_tz.now()
    try:
        result = run_script(s, params)
        execution.status = 'completed'
        execution.result = result if isinstance(result, dict) else {'return': result}
    except Exception:
        execution.status = 'failed'
        execution.error_message = traceback.format_exc()
    finally:
        execution.completed_at = django_tz.now()
        execution.duration = (execution.completed_at - start).total_seconds()
        execution.save()
    return JsonResponse(_execution_to_dict(execution))


# ── Default Parameters ───────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "PUT"])
def default_parameters(request, script_id):
    """GET: 获取脚本缺省参数；PUT: 更新缺省参数"""
    s = get_object_or_404(ScriptDefinition, pk=script_id)
    if request.method == 'GET':
        return JsonResponse({'script_id': s.id, 'default_parameters': s.default_parameters})

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({'error': '请求体必须为有效 JSON'}, status=400)
    s.default_parameters = data.get('default_parameters', data)
    s.save(update_fields=['default_parameters', 'updated_at'])
    return JsonResponse({'script_id': s.id, 'default_parameters': s.default_parameters})


# ── Parameter Presets ────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def presets_list_create(request, script_id):
    """GET: 列出某脚本的参数预设；POST: 创建预设"""
    s = get_object_or_404(ScriptDefinition, pk=script_id)
    if request.method == 'GET':
        qs = s.parameter_presets.all().order_by('name')
        return JsonResponse([_preset_to_dict(p) for p in qs], safe=False)

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({'error': '请求体必须为有效 JSON'}, status=400)
    name = data.get('name')
    if not name:
        return JsonResponse({'error': '缺少 name'}, status=400)
    try:
        p = ScriptParameterPreset.objects.create(
            script=s, name=name, parameters=data.get('parameters', {}),
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse(_preset_to_dict(p), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def preset_detail(request, script_id, preset_id):
    """GET: 预设详情；PUT: 更新；DELETE: 删除"""
    p = get_object_or_404(ScriptParameterPreset, pk=preset_id, script_id=script_id)
    if request.method == 'GET':
        return JsonResponse(_preset_to_dict(p))

    if request.method == 'DELETE':
        p.delete()
        return JsonResponse({'ok': True})

    data = _parse_json_body(request)
    if data is None:
        return JsonResponse({'error': '请求体必须为有效 JSON'}, status=400)
    if 'name' in data:
        p.name = data['name']
    if 'parameters' in data:
        p.parameters = data['parameters']
    try:
        p.save()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse(_preset_to_dict(p))


# ── Categories & Script Files（扫描文件系统）─────────────

@require_GET
def categories_from_db(request):
    """从数据库已有脚本中提取分类列表"""
    cats = list(
        ScriptDefinition.objects.values_list('category', flat=True).distinct().order_by('category')
    )
    return JsonResponse(cats, safe=False)


@require_GET
def categories_available(request):
    """扫描脚本根包下可用的分类（子包列表）"""
    return JsonResponse(scan_categories(), safe=False)


@require_GET
def script_files_in_category(request, category):
    """返回指定分类下的可用脚本文件列表"""
    files = get_script_files(category)
    return JsonResponse(files, safe=False)


# ── Import / Export ──────────────────────────────────────

@csrf_exempt
@require_POST
def import_scripts(request):
    """批量导入脚本定义（JSON 数组）"""
    data = _parse_json_body(request)
    if not isinstance(data, list):
        return JsonResponse({'error': '请求体必须为 JSON 数组'}, status=400)
    created, errors = [], []
    for i, item in enumerate(data):
        try:
            params = item.get('parameters', {})
            default_params = item.get('default_parameters')
            if not default_params and params:
                default_params = {
                    k: v.get('default', '') for k, v in params.items()
                    if isinstance(v, dict) and 'default' in v
                }
            s = ScriptDefinition.objects.create(
                name=item['name'],
                description=item.get('description', ''),
                category=item['category'],
                script_file=item['script_file'],
                parameters=params,
                default_parameters=default_params or {},
            )
            created.append(_script_to_dict(s))
        except Exception as e:
            errors.append({'index': i, 'error': str(e)})
    return JsonResponse({'created': created, 'errors': errors})


@require_GET
def export_scripts(request):
    """导出所有脚本定义为 JSON 数组"""
    qs = ScriptDefinition.objects.all().order_by('category', 'name')
    return JsonResponse([_script_to_dict(s) for s in qs], safe=False)


# ── 预留接口 ─────────────────────────────────────────────

@csrf_exempt
@require_POST
def execute_by_description(request):
    """预留：按自然语言描述执行脚本（本期返回 501）"""
    return JsonResponse({
        'error': '此接口为预留功能，暂未实现。',
        'hint': '后续将集成 LLM，通过自然语言描述匹配并执行脚本。',
    }, status=501)


@csrf_exempt
@require_POST
def query_by_description(request):
    """预留：按自然语言描述查询可用脚本（本期返回 501）"""
    return JsonResponse({
        'error': '此接口为预留功能，暂未实现。',
        'hint': '后续将集成 LLM，通过自然语言描述查询匹配的脚本。',
    }, status=501)
