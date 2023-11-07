# urls.py
from django.urls import path
from . import views
from .views import CustomLoginView

from .views import create_lab
from .views import lab_creation_success

urlpatterns = [
    path('index/', views.index, name='index'),
    path('user_list/', views.user_list, name='user_list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('register/', views.Register.as_view(), name='register'),
    path('book-workstation/', views.BookWorkstation.as_view(), name='book_workstation'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('display-bookings/', views.display_bookings, name='display_bookings'),
    path('available-workstations/', views.available_workstations, name='available_workstations'),

    path('create_lab/', create_lab, name='create_lab'),
    path('lab_creation_success/', lab_creation_success, name='lab_creation_success')

    # Add other URL patterns as needed
]
