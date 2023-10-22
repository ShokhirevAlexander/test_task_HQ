from django.urls import path
from api.views import get_all_lesson, get_lesson, get_product_statistics


urlpatterns = [
     path('get_all_lesson/', get_all_lesson),
     path('get_lesson/', get_lesson),
     path('get_product_statistics/', get_product_statistics),
]
