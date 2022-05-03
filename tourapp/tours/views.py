from django.shortcuts import render
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, TourComment, Tour, TourRating, News, NewsComment, NewsAction
from .serializers import (UserSerializer, CreateTourCommentSerializer, TourSerializer,
                          TourCommentSerializer, TourRatingSerializer, NewsSerializer, NewsCommentSerializer,
                          CreateNewsCommentSerializer, NewsActionSerializer
                          )
from .paginators import TourPaginator
from django.db.models import F
from .perms import CommentOwnerPermisson

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializer

class TourViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Tour.objects.select_related('tour')
    serializer_class = TourSerializer
    pagination_class = TourPaginator
    def get_queryset(self):
        tour = Tour.objects.filter(active = True)

        q = self.request.query_params.get('q')
        if q is not None:
            tour =  Tour.objects.filter(name__icontains = q)
        return tour

    def get_permissions(self):
        if self.action in ['add_comment', 'add-rating']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='add-comment', detail=True)
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = TourComment.objects.create(content=content,
                                       tour_id=self.get_object(),
                                       user_id=request.user)
            return Response(TourCommentSerializer(c).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        tour = self.get_object()
        comments = tour.tourcomments.select_related('user_id').filter(active=True)
        kw = self.request.query_params.get('kw')
        if kw:
            comments = comments.filter(content__icontains=kw)
        return Response(TourCommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='add-rating', detail=True)
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            rate = TourRating.objects.create(rating=rating, tour_id=self.get_object(),
                                         user_id=request.user)
            return Response(TourRatingSerializer(rate).data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='rating', detail=True)
    def get_rating(self, request, pk):
        tour = self.get_object()
        rating = tour.ratings.select_related('user_id').filter(active=True)
        # r = self.request.query_params.get('r')
        # if r:
        #     rating = rating.filter(rating == r)
        return Response(TourRatingSerializer(rating, many=True).data,
                        status=status.HTTP_200_OK)

class TourCommentViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = TourComment.objects.filter(active=True)
    serializer_class = CreateTourCommentSerializer
    ermission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPermisson()]

        return [permissions.IsAuthenticated()]


class NewsViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = News.objects.filter(active = True)
    serializer_class = NewsSerializer

    def get_queryset(self):
        news = News.objects.filter(active=True)

        new = self.request.query_params.get('new')
        if new is not None:
            news = News.objects.filter(subjects__icontains=new)
        return news

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='add-comment', detail=True)
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = NewsComment.objects.create(content=content,
                                           news_id=self.get_object(),
                                           user_id=request.user)
            return Response(NewsCommentSerializer(c).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        new = self.get_object()
        comments = new.newscomments.select_related('user_id').filter(active=True)
        return Response(NewsCommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def add_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError or ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = NewsAction.objects.create(type=action_type, news_id=self.get_object(),
                                           user_id=request.user)
            return Response(NewsActionSerializer(action).data, status=status.HTTP_201_CREATED)


class NewsCommentViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = NewsComment.objects.filter(active=True)
    serializer_class = CreateNewsCommentSerializer
    ermission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPermisson()]

        return [permissions.IsAuthenticated()]


