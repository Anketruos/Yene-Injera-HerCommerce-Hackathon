from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. User model (buyers & sellers)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# 2. Seller details
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name


# 3. Injera model
class Injera(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='injeras')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='injera_images/', blank=True, null=True)
    avg_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.seller.business_name}"


# 4. Ratings model
class Rating(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    injera = models.ForeignKey(Injera, on_delete=models.CASCADE, related_name='ratings')
    texture_rating = models.IntegerField()
    sourness_rating = models.IntegerField()
    color_rating = models.IntegerField()
    overall_rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'injera')  # prevent duplicate ratings

    def __str__(self):
        return f"{self.buyer.username} → {self.injera.name}"

