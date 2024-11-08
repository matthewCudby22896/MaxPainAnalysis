from django.urls import path

from . import views

from Services.MaxPainCharting import MaxPainChartingAPI

urlpatterns = [
    path("", views.index, name="index")
    path('api/ticker/<str:ticker>/', MaxPainChartingAPI.as_view(), name='ticker_details'),
    
]