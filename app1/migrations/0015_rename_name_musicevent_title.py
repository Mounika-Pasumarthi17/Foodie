# Generated by Django 5.1.5 on 2025-02-26 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_rename_title_musicevent_name_musicevent_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='musicevent',
            old_name='name',
            new_name='title',
        ),
    ]
