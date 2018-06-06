from django.urls import path
from .views import ToiletList, ToiletDetail


app_name = 'swacch_toilets'

urlpatterns = [
    path('', ToiletList.as_view(), name="list-toilets"),
    path('<str:pk>', ToiletDetail.as_view(), name="detail-toilet")
]
