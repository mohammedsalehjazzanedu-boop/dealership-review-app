from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # أي رابط تاني (صفحات React مثل /login أو /dealer/1) يخدمه ملف index.html
    # حتى يتولى React Router التوجيه من جانب المتصفح
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]