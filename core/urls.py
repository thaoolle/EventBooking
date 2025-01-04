from django.urls import path
from core import views


app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("event/<str:eid>/", views.event_detail_view, name="event_detail"),
    path('search/', views.search_view, name='search'),
    path('cart/', views.cart_view, name='cart'),
    path('api/events/<str:eid>/', views.event_api, name='event_api'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/success/', views.payment_success_view, name='payment_success'),
    path('api/check-auth/', views.check_auth, name='check_auth'),
    path('api/save-cart/', views.save_cart, name='save_cart'),
    path('process_payment/', views.process_payment, name='process_payment'),
]