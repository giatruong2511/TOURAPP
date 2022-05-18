from django.urls import path, include
from . import views
from rest_framework import routers
from .admin import admin_site

routers = routers.DefaultRouter()
routers.register(prefix='users', viewset=views.UserViewSet, basename='user')
routers.register(prefix='tours', viewset=views.TourViewSet, basename='tour')
routers.register(prefix='tours', viewset=views.TourDetailViewSet, basename='tour')
routers.register(prefix='tourcomments', viewset=views.TourCommentViewSet, basename='tourcomment')
routers.register(prefix='news', viewset=views.NewsViewSet, basename='news')
routers.register(prefix='news', viewset=views.NewsDetailViewSet, basename='news')
routers.register(prefix='newscomments', viewset=views.TourCommentViewSet, basename='newscomment')
routers.register(prefix='bookings', viewset=views.BookingTourViewSet, basename='booking')

urlpatterns = [
    path('', include(routers.urls)),
    path('oauth2-info/', views.AuthInfo.as_view()),
    path('admin/', admin_site.urls),
]