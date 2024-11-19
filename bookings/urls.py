from django.urls import path
from . import views

urlpatterns = [
#     path('loginpage/', views.login_page, name='login_page'),
#     path('adminhome/', views.adminhome, name='adminhome'),
#     path('addpackage/', views.addnewpack, name='addnewpackage'),
#     path('addpackagecategory/', views.addpackcat, name='addpackagecategory'),
#     path('allpackagecategory/', views.allpackcat, name='allpackagecategory'),
#     path('allpackage/', views.allpac, name='allpackage'),
    path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', views.logout_view, name='logout'),
    path('destinations/', views.DestinationListView.as_view(),
         name='destination-list'),
    path('destinations/create/', views.DestinationCreateView.as_view(),
         name='destination-create'),
         path('destinations/edit/<int:pk>/', views.DestinationEditView.as_view(), name='destination-edit'),
    path('destinations/delete/<int:pk>/', views.DestinationDeleteView.as_view(), name='destination-delete'),
    path('packages/', views.PackageListView.as_view(), name='package-list'),
    path('packages/create/', views.PackageCreateView.as_view(),
         name='package-create'),
    path('bookings/create/', views.BookingCreateView.as_view(),
         name='booking-create'),
    path('bookings/confirm/', views.BookingConfirmView.as_view(),
         name='booking-confirm'),  # New confirm endpoint
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(),
         name='booking-detail'),
    path('booking/form/', views.booking_form, name='booking-form'),

    path('properties/', views.PropertyListCreateView.as_view(), name='property-list-create'),
    path('properties/<str:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
]
