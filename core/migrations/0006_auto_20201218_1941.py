# Generated by Django 2.2 on 2020-12-18 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201218_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logistics',
            name='lot',
        ),
        migrations.RemoveField(
            model_name='vaccineproduct',
            name='lot',
        ),
        migrations.AddField(
            model_name='logistics',
            name='lot_num',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.DeleteModel(
            name='Lot',
        ),
    ]
