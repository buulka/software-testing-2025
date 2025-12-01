from django.db import models


class Discount(models.Model):
    coupon_id = models.CharField(primary_key=True, max_length=100)
    amount = models.IntegerField(blank=False, null=False)
    output_amount = models.CharField(blank=False, null=False, max_length=100)

    class Meta:
        managed = True
        db_table = 'discounts'
        verbose_name_plural = 'Скидки'


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True, max_length=500)
    price = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'items'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    items = models.ManyToManyField(Item)
    discount_coupon = models.ForeignKey(Discount, to_field="coupon_id", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'orders'
        verbose_name_plural = 'Заказы'
