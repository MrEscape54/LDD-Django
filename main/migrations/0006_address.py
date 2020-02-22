# Generated by Django 3.0 on 2020-02-07 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200205_0118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='nombre completo')),
                ('address1', models.CharField(max_length=120, verbose_name='dirección 1')),
                ('phone', models.CharField(max_length=20, verbose_name='teléfono')),
                ('zip_code', models.CharField(max_length=12, verbose_name='código postal')),
                ('city', models.CharField(max_length=50, verbose_name='ciudad')),
                ('country', models.CharField(choices=[('AR', 'Argentina'), ('UY', 'Uruguay')], max_length=3, verbose_name='país')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
