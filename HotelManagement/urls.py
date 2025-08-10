"""HotelManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from HotelManagementApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('rooms/',views.rooms,name='rooms'),
    path('login/contact/',views.mail,name='mail'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit-info/', views.edit_profile, name='edit_profile'),
    path('profile/edit-image/', views.edit_profile_image, name='edit_profile_image'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('logout/',views.logout,name='logout'),
    path('adminboard/',views.adminboard,name='adminboard'),
    path('adminboard/rooms/', views.manage_rooms, name='manage_rooms'),
    path('adminboard/rooms/add/', views.add_room, name='add_room'),
    path('adminboard/rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('adminboard/rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('rooms/booking/<int:room_id>/',views.booking,name="booking"),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('adminboard/view-bookings/',views.manage_bookings,name='manage_bookings'),
    path('adminboard/edit-booking/<int:booking_id>/',views.edit_booking,name='edit_booking'),
    path('adminboard/add-booking/',views.add_booking,name='add_booking'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)