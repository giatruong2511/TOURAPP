from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import TourComment, TourRating, User, Tour, NewsComment, NewsAction, News, Category, TourPrice, CustomerType,\
                    Image, BookingTour, Payment



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

class CustomerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerType
        fields = ['name']

class TourPriceSerializer(serializers.ModelSerializer):
    customertype= CustomerTypeSerializer()

    class Meta:
        model = TourPrice
        fields = ['customertype', 'price']
class ImageSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(source='link')
    def get_link(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.link.name

        return request.build_absolute_uri(path)
    class Meta:
        model = Image
        fields = ['link']

class TourSerializer(serializers.ModelSerializer):

     tourprice = TourPriceSerializer(many=True)
     images = ImageSerializer(many=True)
     class Meta:
        model = Tour
        fields = ['id', 'name', 'startingPOS', 'endPOS', 'numberofdays', 'tourprice', 'images']
class TourDetailSerializer(TourSerializer):
    class Meta:
        model = Tour
        fields = TourSerializer.Meta.fields + ['content']

class BookingTourSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tour = TourSerializer()
    class Meta:
        model = BookingTour
        exclude = ['active']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [ 'totalmoney','bookingtour']

class TourCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TourComment
        exclude = ['active']

class CreateTourCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourComment
        fields = ['content', 'user', 'tour']

class CategorySerialzer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    category = CategorySerialzer(many=True)

    def get_image(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)

    class Meta:
        model = News
        fields = ['id', 'subject','content', 'image', 'category']


class NewsCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = NewsComment
        exclude = ['active']

class CreateNewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourComment
        fields = ['content', 'user_id', 'tour_id']


class AuthTourDetailSerializer(TourDetailSerializer):
    rating = serializers.SerializerMethodField()


    def get_rating(self, tour):
        request = self.context.get('request')
        if request:
            r = tour.rating_set.filter(user=request.user).first()
            if r:
                return r.rate

    class Meta:
        model = Tour
        fields = TourDetailSerializer.Meta.fields + ['rating']



class AuthNewsDetailSerializer(NewsSerializer):
    like = serializers.SerializerMethodField()

    def get_like(self, news):
        request = self.context.get('request')
        if request:
            return news.like_set.filter(user=request.user, active=True).exists()


    class Meta:
        model = News
        fields = NewsSerializer.Meta.fields + ['like']



