from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('script-kit/', include('script_kit.urls')),
    path('', RedirectView.as_view(url='/script-kit/', permanent=False)),
]
