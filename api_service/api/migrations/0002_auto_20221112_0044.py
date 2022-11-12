# Generated by Django 3.1.7 on 2022-11-12 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='area_id',
        ),
        migrations.AddField(
            model_name='player',
            name='type',
            field=models.CharField(choices=[('PL', 'Player'), ('CO', 'Coach')], default='PL', max_length=2),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]