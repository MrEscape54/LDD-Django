# Generated by Django 3.0 on 2020-03-10 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_basket_basketline'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='status',
            field=models.IntegerField(choices=[(10, 'Open'), (20, 'Submitted')], default=10),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
