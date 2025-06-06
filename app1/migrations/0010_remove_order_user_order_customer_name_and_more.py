# Generated by Django 5.1.5 on 2025-02-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.CharField(default='unknown product', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='recipient_email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
