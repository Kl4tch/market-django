from django.db import models
from django.utils.text import slugify
from scraper.models import AttributeValue


class Item(models.Model):
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=1000, blank=True, null=True)
    is_enabled = models.BooleanField(default=True)
    viewed = models.IntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True)
    rozetkaUrl = models.CharField(max_length=200, blank=True, null=True)
    priceRozetka = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # small = rescale_image(self.image, width=100, height=100)
        # self.image_small = SimpleUploadedFile(name, small_pic)
        super(Item, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='brand', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Category(models.Model):
    name = models.CharField(max_length=50)
    folder = models.CharField(max_length=20)
    img = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ItemDetail(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    attr = models.ForeignKey('scraper.AttributeValue', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"
    # class Meta:
    #     unique_together = (('attr', 'item'),)

    def __str__(self):
        return str(self.item) + " - " + str(self.attr)


# TODO название property! ProductAttributeValue
    # class Meta:
    #     unique_together = (('attr', 'item'),)


class Image(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    position = models.IntegerField()
    file = models.ImageField(upload_to='media')

    def __str__(self):
        return str(self.item) + " - " + str(self.position)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

