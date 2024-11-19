from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Package, Booking, Destination, Property

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Look for user by username
        user = User.objects.filter(username=data['username']).first()

        if user and user.check_password(data['password']):
            # Generate tokens if user is authenticated
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        
        # If user is not found or password is incorrect
        raise serializers.ValidationError("Invalid credentials")

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'description', 'adult_price', 'child_price']

class DestinationSerializer(serializers.ModelSerializer):
    # packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = ['id', 'name']


class BookingSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'name', 'phone', 'email', 'city', 'package', 'arrival_date', 'departure_date', 
            'num_adults', 'num_children', 'child_ages', 'total_amount'
        ]

    def create(self, validated_data):
        # Override to automatically calculate the total amount when creating a booking
        booking = Booking(**validated_data)
        booking.total_amount = booking.calculate_total_amount()
        booking.save()
        return booking




class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'