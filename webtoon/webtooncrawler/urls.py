from django.urls import path, include
from . import views

# namespcae
app_name = 'webtooncrawler'

urlpatterns = [
    path('index/', views.index, name='index'),
]