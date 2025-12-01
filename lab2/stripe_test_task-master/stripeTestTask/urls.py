from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from stripeApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<int:order_id>/', views.create_session),
    path('order/<int:order_id>/', views.show_order_page),
    path('coupon/', views.create_coupon),
    path('payment_success/<int:order_id>', views.show_success_payment_page),
    path('', views.show_order_list_page)
]

urlpatterns += staticfiles_urlpatterns()
