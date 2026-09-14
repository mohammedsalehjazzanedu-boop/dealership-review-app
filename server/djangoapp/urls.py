from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('register', views.registration, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    path('dealers', views.get_dealerships, name='get_dealerships'),
    path('dealers/state/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('review/add', views.add_review, name='add_review'),

    path('carmakes', views.get_cars, name='get_cars'),
    path('analyze', views.analyze_review_sentiment, name='analyze_review_sentiment'),
]