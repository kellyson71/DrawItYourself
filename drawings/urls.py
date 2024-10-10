from django.urls import path
from .views import drawings_list

urlpatterns = [
    path('', drawings_list, name="main-pa")
]