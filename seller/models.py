from django.db import models

# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=50)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    mob_no = models.IntegerField(blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    pic = models.ImageField(default='defaultUser.png', upload_to='seller_pics')
    
    def __str__(self):
        return self.name