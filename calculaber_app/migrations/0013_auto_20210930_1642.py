# Generated by Django 3.2.6 on 2021-09-30 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0012_auto_20210930_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialobject',
            name='margin',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='materialobject',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=65, null=True),
        ),
    ]
