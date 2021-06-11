# Generated by Django 3.0.5 on 2021-06-11 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normaluser', '0004_blog_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPasswordDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(null=True)),
                ('key', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]