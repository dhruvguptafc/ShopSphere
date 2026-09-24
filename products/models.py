from django.db import models
from django.db.models import DecimalField
from django.core.validators import MinValueValidator 
from decimal import Decimal
# Create your models here.



class Product(models.Model):
    product_name = models.CharField(max_length=100)
    featured_image = models.ImageField(
    upload_to='uploads/%Y/%m/%d',
    blank=True,
    null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name

