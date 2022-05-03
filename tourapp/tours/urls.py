from django.urls import path, include
from . import views
from rest_framework import routers


routers = routers.DefaultRouter()
routers.register(prefix='users', viewset=views.UserViewSet, basename='user')
routers.register(prefix='tours', viewset=views.TourViewSet, basename='tour')
routers.register(prefix='tourcomments', viewset=views.TourCommentViewSet, basename='tourcomment')
routers.register(prefix='news', viewset=views.NewsViewSet, basename='news')
routers.register(prefix='newscomments', viewset=views.TourCommentViewSet, basename='newscomment')


urlpatterns = [
    path('', include(routers.urls))
]