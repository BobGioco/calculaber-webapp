# Generated by Django 3.2.6 on 2021-11-22 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0021_alter_materialtag_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialtag',
            name='tag',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
