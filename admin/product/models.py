from django.db import models
from shared.models import BaseModel
from django.core.validators import MaxLengthValidator


class User(models.Model):
    tg_id = models.CharField(max_length=255)
    username = models.CharField(max_length=50, null=True, blank=True)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    profile_url = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.fullname


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'subcategory'

    def __str__(self):
        return self.name


class Product(BaseModel):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(validators=[MaxLengthValidator(1000)])
    price = models.DecimalField(max_digits=9, decimal_places=2)
    photo_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


class OrderProduct(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        db_table = 'order_product'

    def __str__(self):
        return f"{self.user.fullname} - {self.count} of {self.product.name}"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    exp_time = models.DateTimeField(null=True, blank=True)
    payment = models.BooleanField(default=False)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"{self.user.fullname} - {self.exp_time}"
