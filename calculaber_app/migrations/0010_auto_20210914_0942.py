# Generated by Django 3.2.6 on 2021-09-14 07:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0009_remove_material_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialobject',
            name='create_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='material',
            name='units',
            field=models.CharField(choices=[('0', 'm2'), ('1', 'kus')], default='0', max_length=2),
        ),
    ]
