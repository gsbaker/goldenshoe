# Generated by Django 4.0.6 on 2022-07-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_basketitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitem',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]