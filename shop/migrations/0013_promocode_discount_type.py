# Generated by Django 4.0.6 on 2022-07-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='discount_type',
            field=models.CharField(choices=[('percent', '%'), ('sum', '-')], default='percent', max_length=10),
        ),
    ]
