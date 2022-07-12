from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

STATE_CHOICES =(
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Haryana','Haryana'),
    ('Punjab','Punjab'),
    ('Uter Pardesh','Uter Pardesh'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Gujrat','Gujrat'),
    ('Maharashtra','Maharashtra'),
    ('Bihar','Bihar'),
    ('Himachal Pardesh','Himachal Pardesh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted

    
STATUS_CHOICES = (
      ('Accepted','Accepted'),
      ('Packed','Packed'),
      ('On the way','On the way'),
      ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Accepted')
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted

    


