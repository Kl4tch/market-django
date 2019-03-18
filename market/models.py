from django.db import models
from django.utils.timezone import now


class Item(models.Model):
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000)
    is_enabled = models.BooleanField(default=True)
    price = models.IntegerField()
    viewed = models.IntegerField()
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    count = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Brand(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='brand')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Category(models.Model):
    name = models.CharField(max_length=50)
    folder = models.CharField(max_length=20)
    img = models.ImageField(upload_to='category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class FilterName(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) + " - " + str(self.name)

    class Meta:
        verbose_name = "Атрибут  категории"
        verbose_name_plural = "Атрибуты категории"


class FilterDetail(models.Model):
    name = models.CharField(max_length=30)
    filter = models.ForeignKey('FilterName', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# TODO название property! ProductAttributeValue


class DiscountItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2)

    dateStart = models.DateField(blank=True, null=True)
    dateEnd = models.DateField(blank=True, null=True)

    disc = models.ForeignKey('Discount', on_delete=models.CASCADE, null=True, blank=True)


class Discount(models.Model):
    # TODO картинка для банера акции?
    name = models.CharField(max_length=100, null=True)
    dateStart = models.DateField(default=now())
    dateEnd = models.DateField(default=now())
    img = models.ImageField(upload_to='discounts', null=True, blank=True)

    def __str__(self):
        return "(" + str(self.dateStart) + ' - ' + str(self.dateEnd) + ")"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class ItemDetail(models.Model):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True)
    attr = models.ForeignKey('FilterDetail',
                             on_delete=models.SET_NULL,
                             null=True, )
    value = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = (('attr', 'item'),)

    def __str__(self):
        return str(self.item) + " - " + str(self.attr)


class Image(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    position = models.IntegerField()
    file = models.ImageField(upload_to='media')

    def __str__(self):
        return str(self.item) + " - " + str(self.position)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

