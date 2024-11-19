import uuid
from django.db import models
from django.utils.timezone import now


def generate_custom_id():
    # Generate ID with a prefix (e.g., "ERL") and a random numeric suffix
    return f"ERL{uuid.uuid4().int % 100000:05d}"


class Property(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    number_of_beds = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    amenities = models.TextField(help_text="List of amenities separated by commas")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    custom_id = models.CharField(max_length=10, unique=True, default=generate_custom_id, editable=False)
    image = models.ImageField(upload_to='property_images/')
    post_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
    

class Destination(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Package(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True, related_name='packages')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    adult_price = models.DecimalField(max_digits=10, decimal_places=2)
    child_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.destination:
            return f"{self.destination.name} - {self.name}"
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=255)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="bookings")
    arrival_date = models.DateField()
    departure_date = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    child_ages = models.JSONField(blank=True, null=True, help_text="List of child ages")

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_total_amount(self):
        total = (self.num_adults * self.package.adult_price) + (self.num_children * self.package.child_price)
        return total

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.name} for {self.package.name}"

