from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Restorent(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    address = models.TextField()
    upi_id = models.CharField(max_length=200, blank=True, default="")
    phone_number = models.CharField(max_length=15, blank=True, default="")

    def __str__(self):
        return self.name

class Floor(models.Model):
    name = models.CharField(max_length=100)
    restorent = models.ForeignKey(Restorent, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Table(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, default=1)
    vacent_status = models.BooleanField(default=False)
    order_panding = models.BooleanField(default=True)
    payment_panding = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.floor} ({self.pk})"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restorent = models.ForeignKey(Restorent, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class FoodCategory(models.Model):
    name = models.CharField(max_length=100)
    restorent = models.ForeignKey(Restorent, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class FoodItem(models.Model):
    FOOD_TYPE = [
        ('veg', 'Veg'),
        ('non-veg', 'Non-Veg'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(default=1)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE)
    catogary = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_image = models.ImageField(default='default_food_img.png', upload_to='food_images')

    def __str__(self) -> str:
        return self.name
    
class Tax(models.Model):
    name = models.CharField(max_length=100)
    tax_perscentage = models.FloatField()
    restorent = models.ForeignKey(Restorent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.tax_perscentage}%)"

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    adjustment = models.FloatField(default=0)

    # column create to check whether the food delivered or not
    food_delivered = models.BooleanField(default=False)
    # order maped with the restoren
    restorent = models.ForeignKey(Restorent, on_delete=models.CASCADE, null=True, blank=True)
    
    # delivery details
    # table type, if the order is kind of Delivery then show the user informatoin
    normal_table = models.BooleanField(default=True)
    name = models.CharField(max_length=100, null=True, blank=True, default="")
    phone_number = models.CharField(max_length=15, null=True, blank=True, default="")
    address = models.TextField(default="")

    def generate_transaction_id(self):
        current_time = timezone.now()
        current_time = current_time.strftime('%Y%m%d-%H%m%S')
        transaction_id = f'restorent-{current_time}-{self.id}'
        return transaction_id

    def order_amount(self):
        all_orders = self.items.all()
        amount = 0
        for order in all_orders:
            amount += order.order_price()
        
        return amount

    def complete_amount(self):
        restorent = self.table.floor.restorent
        amount = self.order_amount()
        total_amount = amount
        for tax in restorent.tax_set.all():
            tax_per = tax.tax_perscentage
            tax_amount = amount * (tax_per / 100)
            total_amount += tax_amount
        
        total_amount = round(total_amount, 2)
        total_amount = total_amount + self.adjustment
        total_amount = round(total_amount, 2)
        return total_amount
    
    def __str__(self) -> str:
        return f"Order {self.pk}"

class OrderItems(models.Model):
    FOOD_TYPE = [
        ('veg', 'Veg'),
        ('non-veg', 'Non-Veg'),
    ]
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE)
    item_name = models.CharField(max_length=200)
    item_quantity = models.IntegerField()
    item_price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')


    def __str__(self) -> str:
        return self.item_name

    def order_price(self):
        return self.item_price * self.item_quantity
    
class Payment(models.Model):
    PAYMENT_METHOD = [
        ('CASH', 'CASH'),
        ('UPI', 'UPI'),
        ('CARD', 'CARD'),

    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    paid_amount = models.FloatField() #kitni payment kari h
    timing = models.DateTimeField(auto_now_add=True) # kab payment kari h
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD)
    message = models.TextField(blank=True, null=True)

    