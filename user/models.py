from django.db import models
from market.models import Item
from django.contrib.auth.models import *


# class User(AbstractBaseUser):
#     vk_id = models.CharField(max_length=50)
#     access_token = models.CharField(max_length=100)
#
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     dateCreated = models.DateTimeField(auto_now_add=True)
#
#     USERNAME_FIELD = 'id'
#
#     def __str__(self):
#         return str(self.id)
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#
# class Comment(models.Model):
#     item = models.ForeignKey('market.Item', on_delete=models.CASCADE)
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     text = models.CharField(max_length=500)
#
#     RATE_CHOICES = (
#         ('1', 'Ужасно'),
#         ('2', 'Плохо'),
#         ('3', 'Средний'),
#         ('4', 'Хорошо'),
#         ('5', 'Отлично')
#     )
#     rate = models.CharField(
#         max_length=1,
#         choices=RATE_CHOICES,
#         default='5',
#     )
#
#     reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return str(self.id) + ' - ' + str(self.user) + ' reply on ' + str(self.reply)
#         # return str(self.item) + " - " + str(self.user)
