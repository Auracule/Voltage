from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    STATUS = [
        ('New','New'),
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Sorted','Sorted')
    ]

    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    admin_note = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    message_data = models.DateTimeField(auto_now=True)
    admin_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'


            # email = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=250, default='a')
    img = models.ImageField(upload_to='product', default='prod.jpg')
    price = models.IntegerField()
    max_quantity = models.IntegerField()
    min_quantity = models.IntegerField()
    display = models.BooleanField()
    latest = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Team(models.Model):
    personnel = models.CharField(max_length=50)
    img = models.ImageField(upload_to='team',default='team.jpg')
    post = models.CharField(max_length=50)

    def __str__(self):
        return self.personnel


    class Meta:
        db_table = 'team'
        managed = True
        verbose_name = 'Team'
        verbose_name_plural = 'Team'

class Profile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=50, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pix = models.ImageField(upload_to='profile', default='avatar.jpg')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

class Shopcart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    name_id = models.CharField(max_length=20, default='a', blank=True, null=True)
    amount = models.IntegerField(blank= True, null= True)
    order_no = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.product.name    
        #dunderself