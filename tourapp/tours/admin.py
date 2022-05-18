from datetime import datetime


from django.contrib import admin
from .models import User, Tour, TourRating, \
    TourComment, TourPrice, BookingTour, CustomerType, \
    Tag, Image, Category, News, NewsComment, Payment

from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count, Avg, Sum
from django.contrib.auth.models import Group
from datetime import date





class TourAdmin(admin.ModelAdmin):
    search_fields = ['name', 'endPOS', 'numberofdays']
    list_filter = ['name', 'endPOS', 'numberofdays']


class NewsAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_filter = ['category']


class TourPriceAdmin(admin.ModelAdmin):
    search_fields = ['price']
    list_filter = ['customertype', 'tour']


class TourAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống Tour du lịch'
    def get_urls(self):
        return [
           path('tour-stats/', self.stats_view)
       ] + super().get_urls()

    def stats_view(self, request):
        a = []
        total = []
        totaltour = []
        totalbooking = []
        cars = request.GET.get('cars')
        dau = date.today().year
        if cars == 'nam':
            dau = Payment.objects.filter().first().created_date.year
            a.append(dau)
            cuoi = Payment.objects.filter().last().created_date.year
            a.append(cuoi)
        else:
            a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        count = Tour.objects.filter(active=True).count()
        count_book = BookingTour.objects.filter().count()
        turnover = Payment.objects.filter().aggregate(Sum('totalmoney'))
        if cars == 'nam':
            for i in range(a[0],a[1]+1):
                tien = Payment.objects.filter(created_date__year=i).aggregate(Sum('totalmoney'))
                total.append(tien)
                tour = Tour.objects.filter(created_date__year=i).count()
                totaltour.append(tour)
                booking = BookingTour.objects.filter(created_date__year=i).count()
                totalbooking.append(booking)
        else:
            payment = Payment.objects.filter(created_date__year = date.today().year)
            tours = Tour.objects.filter(created_date__year = date.today().year)
            bookings = BookingTour.objects.filter(created_date__year = date.today().year)
            for i in a:
                tien = payment.filter(created_date__month = i).aggregate(Sum('totalmoney'))
                total.append(tien)
                tour = tours.filter(created_date__month = i).count()
                totaltour.append(tour)
                booking = bookings.filter(created_date__month = i).count()
                totalbooking.append(booking)
        tours = Tour.objects.filter(created_date__month = date.today().month)
        stats = tours\
            .annotate(tourbook_count=Count('my_bookingtour')) \
            .values('id', 'name', 'tourbook_count')

        return TemplateResponse(request, 'admin/tour-stats.html', {
            'tour_count': count,
            'tour_stats': stats,
            'booking_count': count_book,
            'turnover': turnover,
            'cars': cars,
            'a': a,
            'total': total,
            'totaltour': totaltour,
            'totalbooking': totalbooking,
            # 'dau':dau

        })

admin_site = TourAppAdminSite('myadmin')



admin_site.register(User)
admin_site.register(Tour, TourAdmin)
admin_site.register(TourRating)
admin_site.register(TourComment)
admin_site.register(Tag)
admin_site.register(Image)
admin_site.register(Category)
admin_site.register(News, NewsAdmin)
admin_site.register(NewsComment)
admin_site.register(TourPrice, TourPriceAdmin)
admin_site.register(BookingTour)
admin_site.register(CustomerType)
admin_site.register(Payment )
admin_site.register(Group)
