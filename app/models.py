from django.db import models


class Users(models.Model):
    userId = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=300)
    email = models.CharField(max_length=250)
    firstName = models.CharField(max_length=250)


    def __str__(self):
        return 'Users: {}'.format(self.firstName)


class Admin(models.Model):
    userId = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=300)
    email = models.CharField(max_length=250)
    firstName = models.CharField(max_length=250)

    def __str__(self):
        return 'Admin: {}'.format(self.firstName)


class Category(models.Model):
    categoryId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    image = models.ImageField(blank=True)
    def __str__(self):
        return ' {}'.format(self.name)


class Products(models.Model):
    objects = None
    productId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    description = models.CharField(max_length=300)
    image = models.FileField(blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return 'Products: {}'.format(self.name)



class Cart(models.Model):
    userId = models.ForeignKey("Users", on_delete=models.CASCADE)
    productId = models.ForeignKey("Products", on_delete=models.CASCADE)


    def __str__(self):
        return 'Products: {}'.format(self.userId)


class Address(models.Model):
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=250)
    mobile = models.CharField(max_length=250)


    def __str__(self):
        return 'Address: {}'.format(self.email)


class order(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField('medium', max_digits=20, decimal_places=10, blank=True, null=True)
    description = models.CharField(max_length=300)
    image = models.FileField(upload_to='products', null=True, verbose_name="")
    productId = models.IntegerField(null=True)
    userId = models.ForeignKey("Users", on_delete=models.CASCADE)

