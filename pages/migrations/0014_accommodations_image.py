# Generated by Django 3.2.9 on 2022-02-03 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_alter_accommodations_occupancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodations',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
