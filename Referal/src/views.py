
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User

import time
import random
import string

def rm(request):
    return render(request, 'rm.html')

# Функция для проверки кода авторизации и записи пользователя в БД, при необходимости
@api_view(['GET', 'POST'])
def authorize_phone(request):
    # Показать страницу
    if request.method == 'GET':
        return render(request, 'auth.html')
    else:
        phone_number = request.POST.get('phone_number')
        verification_code = random.randint(1000, 9999)
    
        # Здесь должен быть код для проверки кода авторизации, отправленного пользователю
        time.sleep(2)

        # Проверка есть ли пользователь в базе. Если пользователя нет, создаёт и присваивает инвайт код.
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            invite_code = ''.join(random.choices(string.digits + string.ascii_letters, k=6))
            user.invite_code = invite_code
            user.save()
    
        request.session['phone_number'] = phone_number
        request.session.save()
        return redirect('profile')



@api_view(['GET', 'POST'])
def profile(request):
    # Показать страницу
    if request.method == 'GET':
        phone_number = request.session.get('phone_number')
        invited_users = User.objects.filter(invited_by=request.session.get('phone_number'))
        return render(request, 'profile.html', {'inv': invited_users})
    # Обработка введённой информации
    elif request.method == 'POST':
        invited_users = User.objects.filter(invited_by=request.session.get('phone_number'))
        respons = {'inv': invited_users}
        try:
            invite_code = request.POST.get('invite_code')
            phone_number = request.session.get('phone_number')
            user = User.objects.get(phone_number=phone_number)
            # Проверка что пользователь не вводил инвайт код
            if user.invited_by is None:
                user.invited_by = User.objects.get(invite_code=invite_code)
                user.save()
                return render(request, 'profile.html', {'inv': invited_users})
            else:
                return render(request, 'profile.html', {'inv': invited_users, 'error': 'The invite code is already in place.'})
        except User.DoesNotExist:
            return render(request, 'profile.html', {'inv': invited_users, 'error': 'User not found.'})

    

def show_profile(request, phone_number):
     # Найти пользователя с указанным номером телефона
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return redirect('authorize_phone')

    # Отобразить информацию о пользователе
    return render(request, 'show_profile.html', {'user': user})

