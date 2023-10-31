# Generated by Django 4.2.6 on 2023-10-31 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_image',
            field=models.ImageField(blank=True, null=True, upload_to='car-images/'),
        ),
        migrations.AlterField(
            model_name='car',
            name='make',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
