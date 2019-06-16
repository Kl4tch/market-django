from django.db import models
from market.models import *

# Create your models here.


class Store(models.Model):
    COUNTRY_CHOICES = (
        (1, 'ДНР'),
        (2, 'Россия'),
        (3, 'Украина'),
    )
    country = models.IntegerField(
        choices=COUNTRY_CHOICES,
        default=1,
    )

    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return str(f"{self.name} ({self.COUNTRY_CHOICES.__getitem__(self.country-1)[1] })")


class GroupTitle(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Группа характеристик"
        verbose_name_plural = "Группы характеристик"

    def __str__(self):
        return self.title


class AttributeTitle(models.Model):
    bigTitle = models.ForeignKey('GroupTitle', on_delete=models.CASCADE)
    attr = models.CharField(max_length=50)
    isFiltered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Имя характеристики"
        verbose_name_plural = "Имена характеристик"

    def __str__(self):
        return f"{self.attr} ({self.bigTitle.title})"


class AttributeValue(models.Model):
    attributeTitle = models.ForeignKey('AttributeTitle', on_delete=models.CASCADE)
    # item = models.ForeignKey('', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        # return f"{self.value} ({self.attributeTitle.attr})"
        return f"{self.value}"

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значения характеристик"
        unique_together = (('attributeTitle', 'value'),)


class StoreItem(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    item = models.ForeignKey('market.Item', on_delete=models.CASCADE, null=True, blank=True)

    url = models.CharField(max_length=200, blank=True, null=True)

    price = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Товар в магазине"
        verbose_name_plural = "Товары в магазине"

    def __str__(self):
        return f"{self.item.title} {self.store.name} {self.price}"


