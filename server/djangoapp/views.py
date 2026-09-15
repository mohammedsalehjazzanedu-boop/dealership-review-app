import json
import logging

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel, Dealer, Review

logger = logging.getLogger(__name__)


def _dealer_to_dict(dealer):
    return {
        "id": dealer.id,
        "name": dealer.name,
        "short_name": dealer.short_name,
        "full_name": dealer.full_name,
        "city": dealer.city,
        "state": dealer.state,
        "st": dealer.st,
        "address": dealer.address,
        "zip": dealer.zip_code,
        "lat": dealer.lat,
        "long": dealer.long,
    }


# ---------------------------------------------------------
# Task 5: Login
# ---------------------------------------------------------
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)
    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


# ---------------------------------------------------------
# Task 6: Logout
# ---------------------------------------------------------
def logout_request(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')

    username_exist = User.objects.filter(username=username).exists()

    if username_exist:
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Success"})


# ---------------------------------------------------------
# دوال مشتركة (يستخدمها كل من الأسماء القديمة والجديدة)
# ---------------------------------------------------------
def _get_dealers(state="All"):
    if state == "All":
        dealers = Dealer.objects.all()
    else:
        dealers = Dealer.objects.filter(state=state)
    return [_dealer_to_dict(d) for d in dealers]


def get_dealerships(request, state="All"):
    return JsonResponse({"status": 200, "dealers": _get_dealers(state)})


def get_dealer_by_id(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        return JsonResponse({"status": 200, "dealer": _dealer_to_dict(dealer)})
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"})


def get_dealer_reviews(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id)
    reviews_list = list(reviews.values())
    return JsonResponse({"status": 200, "reviews": reviews_list})


# ---------------------------------------------------------
# النسخة الرسمية بأسماء fetchDealers / fetchDealer / fetchReviews
# ---------------------------------------------------------
def fetch_dealers(request):
    return JsonResponse(_get_dealers("All"), safe=False)


def fetch_dealers_by_state(request, state):
    return JsonResponse(_get_dealers(state), safe=False)


def fetch_dealer_by_id(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        return JsonResponse(_dealer_to_dict(dealer), safe=False)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)


def fetch_reviews_by_dealer(request, dealer_id):
    reviews = Review.objects.filter(dealer_id=dealer_id)
    reviews_list = list(reviews.values())
    return JsonResponse(reviews_list, safe=False)


# ---------------------------------------------------------
# إضافة ريفيو
# ---------------------------------------------------------
@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    sentiment = analyze_sentiment_text(data.get("review", ""))

    review = Review.objects.create(
        dealer_id=data["dealer_id"],
        name=data.get("name", request.user.username),
        review=data.get("review", ""),
        purchase=data.get("purchase", False),
        car_make=data.get("car_make", ""),
        car_model=data.get("car_model", ""),
        car_year=data.get("car_year"),
        sentiment=sentiment,
    )

    return JsonResponse({"status": 200, "id": review.id, "sentiment": sentiment})


# ---------------------------------------------------------
# get_cars: تنسيق مسطّح (قائمة أزواج ماركة-موديل)
# ---------------------------------------------------------
def get_cars(request):
    car_models = CarModel.objects.select_related('car_make').all()
    cars = []

    for model in car_models:
        cars.append({
            "CarMake": model.car_make.name,
            "CarModel": model.name,
        })

    return JsonResponse({"CarModels": cars})


def get_cars_nested(request):
    car_makes = CarMake.objects.all()
    result = []

    for make in car_makes:
        models_list = list(make.models.values("id", "name", "type", "year"))
        result.append({
            "id": make.id,
            "name": make.name,
            "description": make.description,
            "models": models_list,
        })

    return JsonResponse({"CarModels": result})


# ---------------------------------------------------------
# تحليل المشاعر
# ---------------------------------------------------------
def analyze_sentiment_text(text):
    if not text:
        return "neutral"

    text_lower = text.lower()

    positive_words = [
        "great", "excellent", "fantastic", "amazing", "good", "happy",
        "love", "best", "wonderful", "friendly", "recommend", "awesome"
    ]
    negative_words = [
        "bad", "terrible", "awful", "worst", "poor", "hate",
        "disappointed", "rude", "horrible", "never again", "unhappy"
    ]

    positive_score = sum(word in text_lower for word in positive_words)
    negative_score = sum(word in text_lower for word in negative_words)

    if positive_score > negative_score:
        return "positive"
    elif negative_score > positive_score:
        return "negative"
    else:
        return "neutral"


def analyze_review_sentiment(request, text=None):
    if text is None:
        text = request.GET.get("text", "")
    sentiment = analyze_sentiment_text(text)
    return JsonResponse({"sentiment": sentiment})