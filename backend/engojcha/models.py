from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# 1. User model (buyers & sellers)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# 2. Seller details
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.business_name


# 3. Injera model
class Injera(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='injeras')
    type = models.CharField(max_length=50, blank=True, null=True)
    type_of_grain = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} by {self.seller.business_name}"


# 4. Ratings model
class Rating(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    injera = models.ForeignKey(Injera, on_delete=models.CASCADE, related_name='ratings')
    texture_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quality_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    freshness_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    on_time_delivery_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    overall_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'injera')

    def __str__(self):
        return f"{self.buyer.username} → {self.injera.type}"


# 5. Order model
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    injera = models.ForeignKey(Injera, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Before saving, check if enough stock exists
        if self.quantity > self.injera.stock_quantity:
            raise ValueError("Not enough injera in stock!")
        
        # Reduce stock
        self.injera.stock_quantity -= self.quantity
        self.injera.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer.username} ordered {self.quantity} of {self.injera.type}"
