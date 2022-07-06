from django.db import models

# Create your models here.


class Product(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=200, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    color = models.CharField(max_length=200, default='')
    brand = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name + ' ({brand})'.format(brand=self.brand)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shoes')

