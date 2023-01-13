import datetime

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from web.forms import AuthForm, UserForm, AdvertForm, EditUserForm, CarForm
from web.models import *

try:
    brands = set([brand[0] for brand in Car.objects.values_list('brand')])
except Exception as ex:
    print(ex)


def main_view(request):
    return redirect('adverts_list')


def adverts_view(request):
    adverts = Advert.objects.all().order_by('-created_at')
    search = request.GET.get('search', '')
    brand = request.GET.get('brand', None)

    if search:
        adverts = adverts.filter(
            Q(car__name__icontains=search) |
            Q(description__icontains=search)
        )

    if brand:
        adverts = adverts.filter(car__brand=brand)

    return render(request, 'web/main.html', {
        'adverts': adverts,
        'search': search,
        'brands': brands,
        'from_fav': False
    })


def advert_view(request, adv_id):
    from_fav = request.GET.get('from_fav', '')
    advert = get_object_or_404(Advert, id=adv_id)
    if request.user.is_authenticated:
        if Favorite.objects.all().filter(user=request.user, advert=advert):
            in_favorite = True
        else:
            in_favorite = False
    else:
        in_favorite = None

    return render(request, 'web/advert.html', {
        'advert': advert,
        'in_favorite': in_favorite,
        'brands': brands,
        'from_fav': from_fav
    })


@login_required
def advert_edit_view(request, adv_id=None):
    form = AdvertForm()
    advert = None
    message = None
    is_add = adv_id

    if adv_id is not None:
        advert = get_object_or_404(Advert, id=adv_id)
        if advert.user != request.user and not request.user.is_superuser:
            return redirect('advert', advert.id)
        form = AdvertForm(instance=advert)

    if request.method == 'POST':
        form = AdvertForm(request.POST, instance=advert)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            car = Car.objects.all().filter(name=cleaned_data['car_name'])
            if car:
                if adv_id:
                    advert = Advert.objects.get(id=adv_id).update(**cleaned_data, user=request.user, car=car[0])
                else:
                    advert = Advert(**cleaned_data, user=request.user, car=car[0])
                    advert.save()
                return redirect('advert', advert.id)
            else:
                message = 'There is no such machine'

    return render(request, 'web/advert_form.html', {
        'id': adv_id,
        'form': form,
        'message': message,
        'brands': brands,
        'is_add': is_add
    })


@login_required
def delete_advert(request, adv_id):
    adv = Advert.objects.get(id=adv_id)
    if request.user == adv.user or request.user.is_staff or request.user.is_superuser:
        adv.delete()
        return redirect('main')
    return redirect('advert_view', adv_id)


def registration_view(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if User.objects.all().filter(email=cleaned_data['email']):
                return render(request, 'web/register.html', {
                    'form': form,
                    'message': 'User with this email already exists!',
                    'brands': brands
                })
            if not cleaned_data['name']:
                cleaned_data['name'] = cleaned_data['email'].split('@')[0]
            user = User.objects.create_user(**cleaned_data)
            login(request, user)

            return redirect('adverts_list')

    return render(request, 'web/register.html', {
        'form': form,
        'brands': brands
    })


def login_view(request):
    form = AuthForm()
    message = None
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = "Email or password entered incorrectly"
            else:
                login(request, user)
                next_url = 'main'
                if 'next' in request.GET:
                    next_url = request.GET.get('next')
                return redirect(next_url)
    return render(request, 'web/login.html', {
        'form': form,
        'message': message,
        'brands': brands
    })


def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def edit_car(request, car_id=None):
    if request.user.is_superuser:
        form = CarForm()
        car = None
        message = None

        if car_id is not None:
            car = get_object_or_404(Car, id=car_id)
            form = CarForm(instance=car)

        if request.method == 'POST':
            form = CarForm(request.POST, instance=car)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                if not Car.objects.all().filter(name=cleaned_data['name']):
                    if car_id:
                        car = Car.objects.get(id=car_id).update(**cleaned_data)
                    else:
                        car = Car(**cleaned_data)
                        car.save()
                    return redirect('main')
                else:
                    message = 'Machine with this name already exists!'

        return render(request, 'web/car_form.html', {
            'id': car_id,
            'form': form,
            'message': message,
            'brands': brands
        })


@login_required
def profile(request):
    return render(request, 'web/profile.html', {'brands': brands})


@login_required
def edit_profile(request):
    form = EditUserForm()
    message = None

    if request.method == 'POST':
        form = EditUserForm(request.POST)

        if form.is_valid():
            if not (User.objects.all().filter(email=form.cleaned_data['email']) and \
                    form.cleaned_data['email'] != request.user.email):
                user = request.user.update(**form.cleaned_data)
                login(request, user)
                return redirect('profile')

            message = 'User with this email already exists!'

    return render(request, 'web/edit_profile.html', {
        'form': form,
        'message': message,
        'brands': brands
    })


@login_required
def favorites(request):
    adverts = Favorite.objects.filter(user=request.user).order_by('-created_at')
    search = request.GET.get('search', '')

    if search:
        adverts = adverts.filter(
            Q(advert__car__name__icontains=search) |
            Q(advert__description__icontains=search)
        )

    adverts = [adv.advert for adv in adverts]

    return render(request, 'web/main.html', {
        'adverts': adverts,
        'search': search,
        'brands': brands,
        'from_fav': True
    })


@login_required
def add_to_favorites(request, adv_id):
    advert = Advert.objects.get(id=adv_id)
    if not Favorite.objects.all().filter(user=request.user, advert=advert):
        favorite = Favorite(user=request.user, advert=advert)
        favorite.save()
    return redirect('advert', adv_id)


@login_required
def delete_from_favorites(request, adv_id):
    advert = Advert.objects.get(id=adv_id)
    adv_in_fav = Favorite.objects.all().filter(user=request.user, advert=advert)
    adv_in_fav.delete()
    return redirect('advert', adv_id)
