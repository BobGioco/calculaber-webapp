# Generated by Django 3.2.6 on 2021-09-09 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0006_material_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='calculaber_app.project'),
        ),
    ]
