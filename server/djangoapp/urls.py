from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('register', views.registration, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    # الأسماء الداخلية القديمة (تُستخدم من واجهة React الحالية)
    path('dealers', views.get_dealerships, name='get_dealerships'),
    path('dealers/state/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer_by_id'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),
    path('review/add', views.add_review, name='add_review'),

    path('carmakes', views.get_cars_nested, name='get_cars_nested'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('analyze', views.analyze_review_sentiment, name='analyze_review_sentiment'),

    # الأسماء الرسمية المطلوبة بالتقييم
    path('fetchDealers', views.fetch_dealers, name='fetch_dealers'),
    path('fetchDealers/<str:state>', views.fetch_dealers_by_state, name='fetch_dealers_by_state'),
    path('fetchDealer/<int:dealer_id>', views.fetch_dealer_by_id, name='fetch_dealer_by_id'),
    path('fetchReviews/dealer/<int:dealer_id>', views.fetch_reviews_by_dealer, name='fetch_reviews_by_dealer'),
    path('analyze/<str:text>', views.analyze_review_sentiment, name='analyze_review_sentiment_path'),
]