from django.urls import path
from . import views

# namespcae
app_name = 'webtooncrawler'

urlpatterns = {
    path('', views.index, name='index'),
}