# Generated by Django 3.2.15 on 2023-09-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
