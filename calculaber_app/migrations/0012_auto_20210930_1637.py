# Generated by Django 3.2.6 on 2021-09-30 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0011_auto_20210928_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialobject',
            name='margin',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='materialobject',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65),
        ),
    ]
