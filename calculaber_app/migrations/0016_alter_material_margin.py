# Generated by Django 3.2.6 on 2021-10-25 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0015_alter_material_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='margin',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=65),
        ),
    ]
