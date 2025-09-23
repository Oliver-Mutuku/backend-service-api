from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "customer"
        verbose_name = "customer"
        verbose_name_plural = "customer"

    def __str__(self):
        return f"{self.name} - ({self.code})"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order"
        verbose_name = "order"
        verbose_name_plural = "order"

    def __str__(self):
        return f"Order #{self.id} -  {self.item} ({self.amount})"

