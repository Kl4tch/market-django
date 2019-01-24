from django.db import models
from market.models import Item


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=150)
    bonus = models.IntegerField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    dateCreated = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField

    def __str__(self):
        return self.name


class Profile(models.Model):
    vk_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.vk_id


class Comment(models.Model):
    item = models.ForeignKey('market.Item', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    rate = models.IntegerField()
    reply = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item) + " - " + str(self.user)


class Cart(models.Model):
    item = models.ForeignKey('market.Item', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    quantity = models.IntegerField()
