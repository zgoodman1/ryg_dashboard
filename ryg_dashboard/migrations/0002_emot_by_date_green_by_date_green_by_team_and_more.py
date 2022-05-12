# Generated by Django 4.0.4 on 2022-05-12 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ryg_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emot_by_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('emotion', models.CharField(max_length=200)),
                ('percentage', models.DecimalField(decimal_places=5, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Green_by_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('percentage', models.DecimalField(decimal_places=5, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='Green_by_team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=200)),
                ('percentage', models.DecimalField(decimal_places=5, max_digits=7)),
            ],
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
