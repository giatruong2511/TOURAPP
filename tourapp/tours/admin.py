from django.contrib import admin
from .models import User, Tour, TourRating, \
    TourComment, TourPrice, BookingTour, CustomerType, \
    Tag, Image, Category, News, NewsComment, Payment

from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count, Avg, Sum


class TourAdmin(admin.ModelAdmin):
    search_fields = ['name', 'endPOS', 'numberofdays']
    list_filter = ['name', 'endPOS', 'numberofdays']

    def get_urls(self):
        return [
                   path('tour-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        count = Tour.objects.filter(active=True).count()
        count_book = BookingTour.objects.filter(active=True).count()
        turnover = Payment.objects.filter(active=True).aggregate(Sum('totalmoney'))
        stats = Tour.objects \
            .annotate(tourbook_count=Count('my_bookingtour')) \
            .values('id', 'name', 'tourbook_count')

        return TemplateResponse(request, 'admin/tour-stats.html', {
            'tour_count': count,
            'tour_stats': stats,
            'booking_count' : count_book,
            'turnover' : turnover
        })


class NewsAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_filter = ['category']


class TourPriceAdmin(admin.ModelAdmin):
    search_fields = ['price']
    list_filter = ['customertype', 'tour']


class TourAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'


admin_site = TourAppAdminSite(name='myadmin')

# class TourAppAdminSite(admin.AdminSite):
#     site_header = 'TourApp'
#
#     def get_urls(self):
#         return [
#             path('tour-stats/', self.stats_view)
#         ] + super().get_urls()
#
#     def stats_view(self, request):
#         count = Tour.objects.filter(active=True).count()
#         stats = Tour.objects \
#                 .annotate(tourbook_count=Count('my_bookingtour')) \
#                 .values('id', 'name', 'tourbook_count')
#
#         return TemplateResponse(request,'admin/tour-stats.html', {
#             'tour_count': count,
#             'tour_stats': stats
#         })
#
# admin_site = TourAppAdminSite(name='myadmin')

admin.site.register(User)
admin.site.register(Tour, TourAdmin)
admin.site.register(TourRating)
admin.site.register(TourComment)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsComment)
admin.site.register(TourPrice, TourPriceAdmin)
admin.site.register(BookingTour)
admin.site.register(CustomerType)
