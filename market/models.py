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
    category = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Image(models.Model):
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    position = models.IntegerField()
    file = models.ImageField(upload_to='media')

    def __str__(self):
        return str(self.item) + " - " + str(self.position)
