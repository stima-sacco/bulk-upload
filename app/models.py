from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255, default="")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CarBrand(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]
    name = models.CharField(max_length=100, unique=True)
    car_brand_date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
def cleanDecimal(value):
    return float(str(value).replace(",", ""))

class Car(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]
    brand = models.ForeignKey(CarBrand, related_name="brand_cars", on_delete=models.CASCADE, default=None)
    vendor = models.CharField(max_length=255, default=None)
    make = models.CharField(max_length=100, unique=False)
    color = models.CharField(max_length=100, default="")
    # weight = models.CharField(max_length=100, default="", blank=True)
    body_type = models.CharField(max_length=100, default="")
    engine_size = models.CharField(max_length=100, default="")
    # engine_size = models.CharField(default="-SELECT ENGINE SIZE-", max_length=255, choices=es.ENGINE_SIZES, help_text=es.ENGINE_SIZES)
    location = models.CharField(max_length=254, default="")
    car_image = models.ImageField(upload_to="car-images/", blank=True, default="")
    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    description = models.TextField(default="")

    STEERING_TYPE_CHOICES = [
        ('-SELECT STEERING TYPE-', 
            (
                ('RHD', 'RHD'),
                ('LHD', 'LHD')
            )
        ),
    ]
    steering_type = models.CharField(default="RHD", max_length=20, choices=STEERING_TYPE_CHOICES)

    CAR_TYPE_CHOICES = [
        ('-SELECT CAR TYPE-', 
            (
                ('NEW CAR', 'NEW CAR'),
                ('LOCALLY USED', 'LOCALLY USED')
            )
        ),
    ]
    car_type = models.CharField(default="NEW", max_length=20, choices=CAR_TYPE_CHOICES)

    TRANSMISSION_TYPE_CHOICES = [
        ('-SELECT TRANSMISSION TYPE-', 
            (
                ('AUTOMATIC', 'AUTOMATIC'),
                ('MANUAL', 'MANUAL')
            )
        ),
    ]
    transmission = models.CharField(default="MANUAL", max_length=20, choices=TRANSMISSION_TYPE_CHOICES)

    FUEL_TYPE_CHOICES = [
        ('-SELECT FUEL TYPE-', 
            (
                ('PETROL', 'PETROL'),
                ('DIESEL', 'DIESEL')
            )
        ),
    ]
    fuel_type = models.CharField(default="PETROL", max_length=20, choices=FUEL_TYPE_CHOICES)

    DRIVE_TYPE_CHOICES = [
        ('-SELECT DRIVE TYPE-', 
            (
                ('2WD', '2WD'),
                ('4WD', '4WD'),
                ('AWD', 'AWD')
            )
        ),
    ]
    drive_type = models.CharField(default="2WD", max_length=10, choices=DRIVE_TYPE_CHOICES)
    
    deposit_on_hire_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    doors = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    mileage = models.IntegerField(default=0)
    year_of_manufacture = models.CharField(max_length=10, default="", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[cleanDecimal])
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[cleanDecimal])
    buyer_name = models.CharField(max_length=100, default="", blank=True)
    buyer_mobile_no = models.CharField(max_length=50, default="", blank=True)
    posting_paid = models.BooleanField(default=False)
    posting_transaction_id = models.CharField(max_length=100, default="INITIAL", blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.make or ''

class ExtraCarImage(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]
    car = models.ForeignKey(Car, related_name="extracarimages", on_delete=models.CASCADE)
    car_image = models.ImageField(upload_to="extra-car-images/", blank=True, null=True)

    def __str__(self):
        return str(self.car_image)
    
    # def save(self, *args, **kwargs):
    #     ut = Utilities()
    #     ut.image_resize(self.car_image, 450, 300)
    #     super().save(*args, **kwargs)