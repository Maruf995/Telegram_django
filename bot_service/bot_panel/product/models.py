from django.db import models

# Create your models here.
class MiniCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'product'    

class Category(models.Model):
    name = models.CharField(max_length=100)
    mini_category = models.ManyToManyField(MiniCategory)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'product'     

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/', blank=True)
    category = models.ManyToManyField(MiniCategory)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'product' 