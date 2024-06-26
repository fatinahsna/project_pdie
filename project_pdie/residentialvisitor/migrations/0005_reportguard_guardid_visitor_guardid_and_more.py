# Generated by Django 4.2.7 on 2024-06-02 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residentialvisitor', '0004_rename_platno_visitor_plateno'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportguard',
            name='guardID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='residentialvisitor.guard'),
        ),
        migrations.AddField(
            model_name='visitor',
            name='guardID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='residentialvisitor.guard'),
        ),
        migrations.AlterField(
            model_name='reportissue',
            name='guardID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='residentialvisitor.guard'),
        ),
        migrations.AlterField(
            model_name='reportissue',
            name='resID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='residentialvisitor.resident'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='resID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='residentialvisitor.resident'),
        ),
    ]
