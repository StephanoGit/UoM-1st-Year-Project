# Generated by Django 4.0 on 2022-03-09 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_merge_20220220_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='location',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='subject',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='internet',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='overall',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='social',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='value_of_money',
            field=models.FloatField(blank=True, null=True),
        ),
    ]