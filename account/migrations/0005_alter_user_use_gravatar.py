# Generated by Django 3.2.5 on 2021-08-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210811_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='use_gravatar',
            field=models.BooleanField(default=False, verbose_name='استفاده از گراواتار'),
        ),
    ]
