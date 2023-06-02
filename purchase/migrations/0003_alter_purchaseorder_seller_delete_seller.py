# Generated by Django 4.2.1 on 2023-06-02 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('purchase', '0002_alter_seller_gstin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='seller.seller'),
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
    ]
