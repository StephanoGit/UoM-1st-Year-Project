# Generated by Django 4.0 on 2022-02-14 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='accommodations',
            name='post_code',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
