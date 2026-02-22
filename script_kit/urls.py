from django.urls import path
from . import views, api

app_name = 'script_kit'

urlpatterns = [
    # 页面
    path('', views.script_kit_view, name='script_kit'),
    path('manage/', views.manage_scripts_view, name='manage_scripts'),

    # API — Scripts CRUD
    path('api/scripts/', api.scripts_list_create, name='api_scripts'),
    path('api/script/<int:script_id>/', api.script_detail, name='api_script_detail'),
    path('api/scripts-list/', api.scripts_simple_list, name='api_scripts_list'),

    # API — Execute
    path('api/execute/', api.execute_script, name='api_execute'),
    path('api/execution/<int:execution_id>/', api.execution_detail, name='api_execution_detail'),

    # API — Default Parameters
    path('api/script/<int:script_id>/default-parameters/', api.default_parameters, name='api_default_parameters'),

    # API — Parameter Presets
    path('api/script/<int:script_id>/presets/', api.presets_list_create, name='api_presets'),
    path('api/script/<int:script_id>/presets/<int:preset_id>/', api.preset_detail, name='api_preset_detail'),

    # API — Categories & Script Files
    path('api/categories/', api.categories_from_db, name='api_categories'),
    path('api/categories-available/', api.categories_available, name='api_categories_available'),
    path('api/script-files/<str:category>/', api.script_files_in_category, name='api_script_files'),

    # API — Import / Export
    path('api/import-scripts/', api.import_scripts, name='api_import_scripts'),
    path('api/export-scripts/', api.export_scripts, name='api_export_scripts'),

    # API — 预留
    path('api/execute-by-description/', api.execute_by_description, name='api_execute_by_description'),
    path('api/query-by-description/', api.query_by_description, name='api_query_by_description'),
]
