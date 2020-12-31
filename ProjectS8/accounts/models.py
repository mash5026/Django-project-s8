from django.db import models

# Create your models here.

class Accounts(models.Model):
    name = models.CharField(max_length=255, null=True)
    mobile = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    mobile_verify = models.BooleanField(null=True)
    cookie = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name


class MobileVerify(models.Model):
    mobile = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=True)


class Category(models.Model):
    category_title = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.category_title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255,null=True)
    price = models.BigIntegerField(max_length=255,null=True)

    def __str__(self):
        return "{} , {} ".format(self.product_title, self.price)


class Order(models.Model):
    account = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,null=True)
    total_price = models.BigIntegerField(max_length=255,null=True)

    def __str__(self):
        return "{} | {} ".format(self.account, self.total_price)

