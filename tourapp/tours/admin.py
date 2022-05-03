from django.contrib import admin
from .models import User, Tour, TourRating,\
        TourComment,TourPrice, BookingTour,CustomerType, \
         Tag, Image, Category, News, NewsComment


admin.site.register(User)
admin.site.register(Tour)
admin.site.register(TourRating)
admin.site.register(TourComment)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(News)
admin.site.register(NewsComment)
admin.site.register(TourPrice)
admin.site.register(BookingTour)
admin.site.register(CustomerType)



