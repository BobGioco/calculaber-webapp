# Generated by Django 3.2.6 on 2021-09-07 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculaber_app', '0002_auto_20210817_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='object',
            name='material',
        ),
        migrations.AddField(
            model_name='object',
            name='name',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='material',
            name='units',
            field=models.CharField(choices=[('0', 'čtvereční metr'), ('1', 'jednotka')], default='0', max_length=2),
        ),
        migrations.CreateModel(
            name='MaterialObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=65)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculaber_app.material')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculaber_app.object')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
