from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    data = {
        "message" : "Hellow World!"
    }
    return JsonResponse(data)
