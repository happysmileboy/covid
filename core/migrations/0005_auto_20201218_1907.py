# Generated by Django 2.2 on 2020-12-18 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201218_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logistics',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Administrator'),
        ),
        migrations.AlterField(
            model_name='logistics',
            name='lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Lot'),
        ),
    ]
