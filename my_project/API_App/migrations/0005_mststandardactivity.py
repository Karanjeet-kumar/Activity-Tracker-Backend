# Generated by Django 5.0.14 on 2025-05-23 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_App', '0004_mstcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MstStandardActivity',
            fields=[
                ('sa_id', models.AutoField(primary_key=True, serialize=False)),
                ('activity_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField()),
                ('created_by', models.CharField(blank=True, max_length=10, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(db_column='category_id', on_delete=django.db.models.deletion.CASCADE, to='API_App.mstcategory')),
            ],
            options={
                'db_table': 'Mst_StandardActivity',
            },
        ),
    ]
