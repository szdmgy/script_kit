from django.urls import path
from . import views

app_name = 'script_kit'

urlpatterns = [
    path('', views.script_kit_view, name='script_kit'),
    path('manage/', views.manage_scripts_view, name='manage_scripts'),
]
