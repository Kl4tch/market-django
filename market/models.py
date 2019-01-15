from django.db import models


class Items(models.Model):
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000)
    is_enabled = models.BooleanField(default=True)
    price = models.IntegerField()
    viewed = models.IntegerField()
    rate = models.DecimalField(max_digits=2, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
