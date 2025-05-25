from django.db import models
from product.models import Product

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True,blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    number = models.CharField(max_length=20, blank=True, null=True)  # Лучше CharField для номеров телефонов
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.second_name}' if self.first_name or self.second_name else str(self.telegram_id)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.product.name} x {self.quantity} for {self.user.telegram_id}'


class MailingList(models.Model):
    text = models.TextField(max_length=500)
    time = models.TimeField()

    def __str__(self):
        return self.text


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.telegram_id}"