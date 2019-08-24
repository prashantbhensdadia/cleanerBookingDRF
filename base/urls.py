from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^signup', UserCreateView.as_view()),
    url(r'^get_city_list', GetCityList.as_view()),
    url(r'^create/cleaner', CleanerCreateView.as_view()),
]