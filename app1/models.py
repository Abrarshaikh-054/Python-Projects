from django.db import models
from django.utils import timezone
from django.db.models import JSONField

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    password = models.CharField(max_length=8)
    usertype = models.CharField(max_length=10,default="customer")

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    uname = models.CharField(default="username",max_length=10)
    profile = models.ImageField(default="static/images/user.svg",upload_to="pictures/")
    address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('male','Male'),
        ('female','Female'),
        ('other','Other'),
    ]
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,blank=True, null=True)

    def __str__(self):
        return self.user.name
    
class Product(models.Model):

    PRODUCT_CATEGORIES = [
        ('chair','Chair'),
        ('sofa','Sofa'),
    ]
    seller = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'usertype': 'seller'})
    pcat = models.CharField(max_length=10,choices=PRODUCT_CATEGORIES)
    pname = models.CharField(max_length=30)
    pcaption = models.CharField(max_length=50,blank=True,null=True)
    pdesc = models.TextField(max_length=500,blank=True,null=True)
    pprice = models.FloatField(blank=True,null=True)
    pimg = models.ImageField(default="",upload_to="product_images/")
    color = models.CharField(max_length=20, blank=True, null=True)
    material = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.pname
    
class Wishlist(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} - {self.product.pname}"
    
class Cart(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    payment = models.BooleanField(default=False)
    pqty = models.PositiveIntegerField(default=1)
    pttl = models.FloatField(blank=True,null=True)
    cttl = models.FloatField(blank=True,null=True)

    def save(self, *args, **kwargs):
        self.pttl = self.product.pprice * self.pqty
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.name} - {self.product.pname}"
    
class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing = models.ForeignKey(BillingDetails, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.billing.user.name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.pname}"  