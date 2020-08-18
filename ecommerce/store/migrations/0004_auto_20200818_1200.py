# Generated by Django 3.1 on 2020-08-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite', to='store.Customer'),
        ),
        migrations.AddField(
            model_name='product',
            name='label',
            field=models.CharField(blank=True, choices=[('OUT OF STOK', 'OUT OF STOKn'), ('NEW', 'NEW')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='nb_products',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
