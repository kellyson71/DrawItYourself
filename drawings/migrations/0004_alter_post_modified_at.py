# Generated by Django 5.1.1 on 2024-10-21 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawings', '0003_alter_post_author_alter_post_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]