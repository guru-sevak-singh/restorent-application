from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from webpush import send_user_notification
from webpush import send_group_notification
import json

def send_push_notification(request):
    # user = User.objects.get(username="guru")  # Replace with the actual username
    user = User.objects.first()
    payload = {
        "head": "New Notification",
        "body": "You have a new message!",
        "icon": "https://guru-sevak-singh.github.io/scan2food-static/static/assets/images/brand/Scan2FoodFabIcon.png",
        "url": "/dashboard/"  # Redirect URL when clicked
    }

    send_user_notification(user=user, payload=payload, ttl=1000)
    return JsonResponse({'status': True})

def send_perticular_user(request, pk):
    payload = {
        "head": "New Update!",
        "body": "Check out our latest feature.",
        "icon": "https://guru-sevak-singh.github.io/scan2food-static/static/assets/images/brand/Scan2FoodFabIcon.png",
        "url": "/dashboard/"
    }
    try:
        user = User.objects.get(pk=pk)
        send_user_notification(user=user, payload=payload, ttl=1000)
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': "user not present"})