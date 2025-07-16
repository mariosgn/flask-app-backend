from django.urls import path
from .views import media_post, media_get, HomeView

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('media_post/', media_post, name='media_post'),
    path('media_get/', media_get, name='media_get'),
]