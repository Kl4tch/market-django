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
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    folder = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ItemAttribute(models.Model):
    item = models.ForeignKey('Items', on_delete=models.SET_NULL, null=True)
    attr = models.ForeignKey('Atribute', on_delete=models.SET_NULL, null=True)
    value = models.CharField(max_length=30)

    def __str__(self):
        return str(self.item) + " - " + str(self.attr)


class Atribute(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) + " - " + str(self.name)


class Image(models.Model):
    item = models.ForeignKey('Items', on_delete=models.CASCADE)
    position = models.IntegerField()
    file = models.ImageField(upload_to='media')

    def __str__(self):
        return str(self.item) + " - " + str(self.position)
