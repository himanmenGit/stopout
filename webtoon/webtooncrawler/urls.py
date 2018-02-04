from django.urls import path, include
from . import views

# namespcae
app_name = 'webtooncrawler'

urlpatterns = [
    path('', views.webtoon_list, name='list'),
    path('<int:webtoon_pk>/', views.webtoon_detail, name='detail'),
]