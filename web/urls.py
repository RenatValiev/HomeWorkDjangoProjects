"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from web.views import main_view, adverts_view, advert_view, add_to_favorites, delete_from_favorites, \
    registration_view, login_view, logout_view, profile, favorites, edit_profile, advert_edit_view, delete_advert, \
    edit_car

urlpatterns = [
    path("", main_view, name='main'),
    path('adverts/', adverts_view, name='adverts_list'),
    path('adverts/<int:adv_id>/', advert_view, name='advert'),
    path('adverts/add/', advert_edit_view, name='add_advert'),
    path('adverts/<int:adv_id>/edit/', advert_edit_view, name='edit_advert'),
    path('adverts/<int:adv_id>/delete/', delete_advert, name='delete_advert'),
    path('favorites/', favorites, name='favorites'),
    path('adverts/<int:adv_id>/add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('adverts/<int:adv_id>/delete_from_favorites/', delete_from_favorites, name='delete_from_favorites'),
    path('sign_up/', registration_view, name='registration'),
    path('log_in/', login_view, name='login'),
    path('log_out/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('cars/add/', edit_car, name='add_car'),
    path('cars/<int:car_id>/edit/', edit_car, name='edit_car')
]
