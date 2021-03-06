# Generated by Django 2.1.3 on 2021-04-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dis_calc', '0002_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='user_with_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('has_reports', models.CharField(max_length=100)),
                ('prs_report', models.CharField(max_length=100)),
                ('dis_report', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Upload',
        ),
    ]
