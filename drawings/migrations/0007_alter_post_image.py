# Generated by Django 5.1.1 on 2024-12-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0006_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
