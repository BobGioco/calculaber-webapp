# Generated by Django 3.2.6 on 2021-09-09 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculaber_app', '0005_remove_material_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calculaber_app.project'),
        ),
    ]
