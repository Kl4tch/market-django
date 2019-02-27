from django.db import models
from django.template.defaultfilters import slugify

# TODO base с датами
# TODO offer
# TODO посты


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
    # TODO ПРОДУМАТЬ СЛАГ
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
    # TODO загрузка картинок по категориям
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
    # TODO оптимизация картинки для отображения
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    position = models.IntegerField()
    file = models.ImageField(upload_to='media')

    def __str__(self):
        return str(self.item) + " - " + str(self.position)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

