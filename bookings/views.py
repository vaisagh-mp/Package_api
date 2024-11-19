from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from .models import Package, Booking, Destination
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookingSerializer, PackageSerializer, BookingSerializer, DestinationSerializer, LoginSerializer
from django.conf import settings
import razorpay
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import Property
from .serializers import PropertySerializer

# # Login page view
# def login_page(request):
#     return render(request, 'superuser/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login_page')

# # admin page view
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def adminhome (request):
#     return render(request, 'superuser/adminhome.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def addnewpack (request):
#     return render(request, 'superuser/addnewpackage.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def addpackcat (request):
#     return render(request, 'superuser/addpackagecategory.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def allpackcat (request):
#     return render(request, 'superuser/allpackagecategories.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def allpac (request):
#     return render(request, 'superuser/allpackages.html')


# login view
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Send back tokens and username
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin-only permission class


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# Destination list view


class DestinationListView(generics.ListAPIView):
    queryset = Destination.objects.all().prefetch_related('packages')
    serializer_class = DestinationSerializer

# Destination create view (admin only)


class DestinationCreateView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestinationEditView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk, *args, **kwargs):
        try:
            destination = Destination.objects.get(pk=pk)
        except Destination.DoesNotExist:
            return Response({"error": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DestinationSerializer(destination, data=request.data, partial=True)  # Use `partial=True` for partial updates.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestinationDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk, *args, **kwargs):
        try:
            destination = Destination.objects.get(pk=pk)
        except Destination.DoesNotExist:
            return Response({"error": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)

        destination.delete()
        return Response({"message": "Destination deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


def booking_form(request):
    return render(request, 'bookings/booking_form.html')

# Package list view


class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageCreateView(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAdminUser]


# Booking creation view
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Booking detail view


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')

        # Verify the payment signature
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Update booking status to confirmed
        try:
            booking = Booking.objects.get(id=booking_id)
            # Assuming 'confirmed' is a status field in Booking model
            booking.status = 'confirmed'
            booking.save()
            return Response({"message": "Booking confirmed successfully"}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)



class PropertyListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PropertyDetailView(APIView):
    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return None

    def put(self, request, pk, *args, **kwargs):
        property_instance = self.get_object(pk)
        if not property_instance:
            return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(property_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        property_instance = self.get_object(pk)
        if not property_instance:
            return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

        property_instance.delete()
        return Response({"message": "Property deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
