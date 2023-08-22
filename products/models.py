from django.db import models
from users.models import User
import uuid


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = [
        ("AVAILABLE", "Available"),
        ("BOOKED", "Booked"),
        ("BORROWED", "Borrowed")
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default="AVAILABLE")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    RESERVATION_STATUS = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("DECLINED", "Declined")
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product', default=None)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester', null=True, blank=True)
    status = models.CharField(max_length=10, choices=RESERVATION_STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.product} by {self.requester}"


