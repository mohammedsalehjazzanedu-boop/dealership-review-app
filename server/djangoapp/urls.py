from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from djangoapp import views as djangoapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # نفس الروابط الرسمية لكن بدون بادئة djangoapp/ (لتطابق التسمية الرسمية بالضبط)
    path('fetchDealers', djangoapp_views.fetch_dealers, name='fetch_dealers_root'),
    path('fetchDealers/<str:state>', djangoapp_views.fetch_dealers_by_state, name='fetch_dealers_by_state_root'),
    path('fetchDealer/<int:dealer_id>', djangoapp_views.fetch_dealer_by_id, name='fetch_dealer_by_id_root'),
    path('fetchReviews/dealer/<int:dealer_id>', djangoapp_views.fetch_reviews_by_dealer, name='fetch_reviews_root'),
    path('djangoapp/analyze/<str:text>', djangoapp_views.analyze_review_sentiment, name='analyze_path_root'),

    # أي رابط تاني (صفحات React) يخدمه ملف index.html
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]