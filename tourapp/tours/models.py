from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')

class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Tour(ModelBase):
    name = models.CharField(max_length=255, null=False)
    startingPOS = models.CharField(max_length=255,blank=True)
    endPOS = models.CharField(max_length=255, null=False)
    startdate = models.DateTimeField(null= False)
    numberofdays = models.IntegerField(null= False)
    content = RichTextField()

    def __str__(self):
        return self.name


class CustomerType(ModelBase):
    name = models.CharField(max_length=255, null=False,  unique=True)
    def __str__(self):
        return self.name

class TourPrice(ModelBase):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tourprice')
    customertype = models.ForeignKey(CustomerType, on_delete=models.CASCADE, related_name='customer')
    price = models.IntegerField(null=False)
    class Meta:
        unique_together = ('tour', 'customertype')

    def __str__(self):
        return self.tour.name + " " + self.customertype.name

class BookingTour(ModelBase):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookingtour', related_query_name='my_bookingtour')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    bookingdate = models.DateTimeField(auto_now_add=True)
    childticketnumber = models.IntegerField(default = 0, null=False)
    adultticketnumber = models.IntegerField(default=1, null=False)

    def __str__(self):
        return self.tour.name + " " + str(self.user)

class Payment(ModelBase):
    bookingtour = models.ForeignKey(BookingTour, null=True, on_delete=models.SET_NULL)
    totalmoney = models.FloatField()

class Tag(ModelBase):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

class Image(ModelBase):
    name = models.CharField(max_length=255, null=False)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images', related_query_name='my_image')
    link = models.ImageField(upload_to='images/%Y/%m/',
                              null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True,
                                  related_name='images')

    def __str__(self):
        return self.name

class TourComment(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tourcomments')
    content = RichTextField()
    def __str__(self):
        return self.content

class TourRating(ModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(null=False)

    def __str__(self):
        return self.tour.name + " " + str(self.rating)

class Category(ModelBase):
    name = models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.name

class News(ModelBase):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='news/%Y/%m/',
                              null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True,
                                  related_name='news')
    def __str__(self):
        return self.subject

class NewsComment(ModelBase):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='newscomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    def __str__(self):
        return self.content

class NewsAction(ModelBase):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    LIKE, HAHA, HEART, SAD = range(4)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart'),
        (SAD, 'sad')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)
