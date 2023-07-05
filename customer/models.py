from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    gstin = models.CharField(max_length=15)
    address1 = models.TextField()
    address2 = models.TextField()
    mob_no = models.IntegerField(blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    pic = models.ImageField(default='defaultUser.png', upload_to='customer_pics')
    
    def __str__(self):
        return self.name