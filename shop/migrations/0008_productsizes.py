# Generated by Django 4.0.6 on 2022-07-06 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_productsize'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.product')),
                ('sizes', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.productsize')),
            ],
        ),
    ]
