# Generated by Django 5.0.1 on 2024-01-19 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='created_ad',
            new_name='created_at',
        ),
    ]
