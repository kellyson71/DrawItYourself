# Generated by Django 5.1.1 on 2024-11-11 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0006_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
