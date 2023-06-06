# Generated by Django 4.2.1 on 2023-06-04 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_product_measuring_unit_2_and_more'),
        ('purchase', '0003_alter_purchaseorder_seller_delete_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderdescription',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_product', to='inventory.product'),
        ),
    ]
