from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # أي رابط تاني (صفحات React) يخدمه ملف index.html
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]