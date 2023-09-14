from django.db import models
from django.contrib.auth.models import User
from .Managers import MyManager

ch=(
    ('dt','Dresses'),
    ('je','Jeans'),
    ('ja','Jackets'),
    ('sh','Shirts'),
    ('te','Tees'),
    ('wa','Watch'),
    ('su','Sunglass'),
    ('ca','Candles'),
)
class Product(models.Model):
    name=models.CharField(max_length=100)
    sellingprice=models.FloatField()
    description=models.TextField()
    discountedprice=models.FloatField()
    quantity=models.IntegerField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=ch,max_length=3)
    image=models.ImageField(upload_to="productimg")
    objects=models.Manager()
    products=MyManager()
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    # discountedprice=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)

    def totalamount(self):
        return self.quantity * self.product.discountedprice

class ItemModel(models.Model):
    name = models.CharField(max_length = 100)
    amount = models.IntegerField()
    order_id = models.CharField(max_length = 100)
    razorpay_payment_id = models.CharField(max_length = 100,blank=True)
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.name+" "+str(self.amount)

    


