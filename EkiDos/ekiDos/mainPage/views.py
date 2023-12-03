from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.db.models import Q
from .forms import CommentForm
from django.contrib.auth.decorators import login_required   
from django.urls import reverse     
from django.http import HttpResponseRedirect, HttpResponse
import requests
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from .models import *
from .forms import *

def index(request):
    fastfood = Dish.objects.all()
    fastfoodCategory = FoodCategory.objects.all()
    comment_count = Comments.objects.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            comment_count += 1
            return redirect('mainPage:chat')
    else:
        form = CommentForm()

    response = requests.get('https://ipinfo.io')
    city = response.json().get('city', 'Unknown City')

    response = requests.get('http://worldtimeapi.org/api/ip')
    current_time = datetime.fromisoformat(response.json()['datetime']).strftime('%Y-%m-%d %H:%M:%S')

    api_key = '674e9f7aff53df244de011df3f3c6e97'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=params)
    data = response.json()
    curr_weather = data['main']['temp']

    comments = Comments.objects.all()
    context = {
        'fastfood': fastfood,
        'fastfoodCategory': fastfoodCategory,
        'comment_count' : comment_count,
        'comments': comments,
        'comment_form': form,
        'comment_count': comment_count,
        'city':city,
        'current_time' :current_time,
        'curr_weather' : curr_weather,
    }
    

    return render(request, 'mainPage/index.html', context)

def logout_view(request):
    logout(request)
    return redirect('mainPage:index')

def search_view(request):
    query = request.GET.get('query', '')
    
    results = Dish.objects.filter(name__icontains=query)
    context = {'results': results, 'query': query, }
    
    return render(request, 'mainPage/search_results.html', context)

def chatView(request):
    comment_count = Comments.objects.count()
    sort_option = request.GET.get('sort_option', 'newest')

    if sort_option == 'newest':
        comments = Comments.objects.all().order_by('-created_at')
    elif sort_option == 'oldest':
        comments = Comments.objects.all().order_by('created_at')
    elif sort_option == 'like': 
        comments = Comments.objects.all().order_by('-likes')
    else:
        comments = []

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            return redirect('mainPage:chat')
    else:
        form = CommentForm()

    context = {
        'user': request.user,
        'comment_form': form,
        'comment_count': comment_count,
        'comments': comments,
        'sort_option': sort_option,
    }

    return render(request, 'mainPage/chat.html', context)


@login_required
def like_comment(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    
    if request.GET.get('action') == 'like':
        comment.likes += 1
        comment.save()
    elif request.POST.get('action') == 'sort':
        return redirect('chat', sort_option=request.POST.get('sort_option', 'newest'))

    return HttpResponseRedirect(reverse('mainPage:chat'))


def view_cart(request):
    user = request.user

    cart, created = Cart.objects.get_or_create(user=user)

    products_in_cart = cart.dishes.all()

    total_price = 0
    total_price_all = 0
    if products_in_cart:
        total_price = cart.dishes_total_price()
        total_price_all = int(total_price) + 150


    context = {
        "products_in_cart":products_in_cart,
        'total_price':total_price,
        'total_price_all':total_price_all,
    }

    return render(request, 'mainPage/view_cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        dish = Dish.objects.get(id=dish_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.dishes.add(dish)

        

    return redirect('mainPage:index')

def delete_product_in_cart(request, product_id):
    user = request.user

    cart, created = Cart.objects.get_or_create(user=user)

    product = get_object_or_404(Dish, id=product_id)

    cart.dishes.remove(product)

    return redirect('mainPage:view_cart')
    
@login_required
def profile(request):
    user = request.user
    add_profile_attr, created = AddProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = AddProfileForm(request.POST, request.FILES, instance=add_profile_attr)
        if form.is_valid():
            form.save()

    return render(request, 'mainPage/profile.html', {'user': user, 'add_profile_attr': add_profile_attr})

@login_required
def add_profile(request):
    user_id = request.user.id
    existing_profile = AddProfile.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if existing_profile:
            existing_profile.first_name = first_name
            existing_profile.last_name = last_name
            existing_profile.img = avatar
            existing_profile.save()
        else:
            profile = AddProfile(user=request.user, first_name=first_name, last_name=last_name, img=avatar)
            profile.save()

        return redirect('mainPage:profile')  

    return render(request, 'mainPage/add_profile.html')

@csrf_exempt
def send_to_telegram(request):
    if request.method == 'POST':
        data = request.POST.get('data', None)

        if data:
            try:
                data_dict = json.loads(data)
                message = "Новый заказ:\n"

                for item in data_dict:
                    message += f"{item['dish_id']} - {item['count']} шт.\n"

                # Отправка сообщения в телеграм
                telegram_bot_token = '6412022902:AAEDaK6p-D7LBrJuz6PgpsBvIjwgpq4BC3U'
                chat_id = '6412022902'
                telegram_api_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
                params = {'chat_id': chat_id, 'text': message}
                requests.post(telegram_api_url, params=params)

                return JsonResponse({'success': True})
            except json.JSONDecodeError as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No data provided'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

