# fullstack_developer_capstone

مشروع Capstone - تطبيق ويب لعرض تفاصيل معارض السيارات (Dealers) وتقييمات العملاء (Reviews) الخاصة فيها، مبني باستخدام Django كـ Backend و React كـ Frontend.

## نظرة عامة

هذا التطبيق يسمح للمستخدمين بـ:
- تصفح قائمة معارض السيارات (Dealers) وتفاصيلها
- فلترة المعارض حسب الولاية (State)
- عرض تقييمات العملاء لكل معرض
- تسجيل الدخول وإنشاء حساب جديد
- إضافة تقييم جديد لأي معرض
- تحليل مشاعر التقييم (Sentiment Analysis) تلقائياً

## التقنيات المستخدمة

- **Backend:** Django, Django REST Framework
- **Frontend:** React
- **Database:** SQLite
- **Deployment:** Render
- **CI/CD:** GitHub Actions

## هيكلية المشروع

```
xrwvm-fullstack_developer_capstone/
├── server/
│   ├── djangoproj/
│   ├── djangoapp/
│   ├── frontend/
│   │   ├── static/
│   │   └── src/
│   └── manage.py
└── README.md
```

## طريقة التشغيل

1. تثبيت متطلبات Python: `pip install -r requirements.txt`
2. تشغيل السيرفر: `python manage.py runserver`
3. تثبيت متطلبات React: `npm install` (داخل مجلد frontend)
4. تشغيل الواجهة: `npm start`