# Generated by Django 4.0.6 on 2023-09-24 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='a_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='activity.activitytype'),
        ),
    ]