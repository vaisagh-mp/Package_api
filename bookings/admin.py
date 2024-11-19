from django.contrib import admin
from .models import Package, Booking, Destination, Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'post_date')
    search_fields = ('title', 'location')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'adult_price', 'child_price')
    search_fields = ('name', 'destination__name')
    ordering = ('name',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'package', 'arrival_date', 'departure_date', 'num_adults', 'num_children', 'total_amount')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('package', 'arrival_date', 'departure_date')
    ordering = ('arrival_date',)

# Register your models here
admin.site.register(Package, PackageAdmin)
admin.site.register(Booking, BookingAdmin)
