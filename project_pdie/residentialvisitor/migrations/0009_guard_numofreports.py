# Generated by Django 4.2.7 on 2024-06-13 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residentialvisitor', '0008_guard_guardpost_guard_guardshift'),
    ]

    operations = [
        migrations.AddField(
            model_name='guard',
            name='numOfReports',
            field=models.IntegerField(default=0),
        ),
    ]
