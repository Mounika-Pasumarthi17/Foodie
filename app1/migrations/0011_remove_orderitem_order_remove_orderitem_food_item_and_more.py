# Generated by Django 5.1.5 on 2025-02-20 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_remove_order_user_order_customer_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='food_item',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
