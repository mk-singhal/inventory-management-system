from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=20)
    pic = models.ImageField(default='defaultProduct.png', upload_to='product_pics')
    hsn_code = models.IntegerField()
    qty = models.IntegerField()
    min_stock_alarm = models.IntegerField(default=20)
    measuring_unit_1 = models.CharField(max_length=20)   # Measuring Unit-Smallest
    measuring_unit_2 = models.CharField(max_length=20, blank=True, null=True)   # Measuring Unit
    measuring_unit_relation = models.IntegerField(null=True, blank=True)
    price = models.FloatField()
    gst = models.IntegerField()
     
    def __str__(self):
        return self.name