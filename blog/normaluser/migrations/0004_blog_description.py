# Generated by Django 3.0.5 on 2021-06-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normaluser', '0003_auto_20210611_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.TextField(null=True),
        ),
    ]