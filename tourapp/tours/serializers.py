from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import TourComment, TourRating, User, Tour, NewsComment, NewsAction, News, Category



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username', 'password', 'email', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        data = validated_data.copy()
        user =User(**data)
        user.set_password(user.password)
        user.save()

        return user


class TourSerializer(serializers.ModelSerializer):

     class Meta:
        model = Tour
        fields = ['id', 'name', 'startingPOS', 'endPOS', 'numberofdays']

class TourCommentSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = TourComment
        exclude = ['active']

class CreateTourCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourComment
        fields = ['content', 'user_id', 'tour_id']

class TourRatingSerializer(ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = TourRating
        exclude = ['active']

class CategorySerialzer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerialzer(many=True)
    class Meta:
        model = News
        fields = ['id', 'subject', 'content', 'image', 'category']


class NewsCommentSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = NewsComment
        exclude = ['active']

class CreateNewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourComment
        fields = ['content', 'user_id', 'tour_id']


class NewsActionSerializer(ModelSerializer):
    class Meta:
        model = NewsAction
        fields = ['id', 'type', 'created_date']



