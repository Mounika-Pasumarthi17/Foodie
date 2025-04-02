from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
from django.conf import settings

# User=get_user_model()

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.username



class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='food_images/')
    
    # New field for manually adding ratings
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # Example: 4.5, 3.8, etc.

    def __str__(self):
        return f"{self.name} - {self.rating}★"


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurant_images/')
    description = models.TextField(null=True, blank=True)  # Allowing it to be optional
    location = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    contact = models.CharField(max_length=15, default="Not Available")  # Default contact number
    opening_hours = models.CharField(max_length=100, null=True, blank=True)
    closing_hours = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} - {self.quantity}"
    

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} ({self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_items = models.ManyToManyField(FoodItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="order_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.food_item.name} ({self.quantity})"



class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_request = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking by {self.user.username} at {self.restaurant.name} on {self.date} {self.time}"


class MusicEvent(models.Model):
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='music_events/')
    # description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.title

class ShowBooking(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    show_name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.show_name}"
    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name