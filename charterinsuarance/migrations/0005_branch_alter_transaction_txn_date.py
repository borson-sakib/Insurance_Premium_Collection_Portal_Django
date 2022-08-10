# Generated by Django 4.0.4 on 2022-07-14 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charterinsuarance', '0004_alter_transaction_txn_date_alter_user_employeeid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_code', models.CharField(max_length=7, null=True, unique=True)),
                ('branch_name', models.CharField(max_length=200)),
                ('is_branch', models.BooleanField(default=True)),
                ('branch_mnemonic', models.CharField(max_length=7, null=True)),
                ('sbs_code', models.CharField(max_length=50, null=True)),
                ('branch_address', models.CharField(max_length=450, null=True)),
                ('created_by', models.CharField(max_length=450, null=True)),
                ('creat_date', models.CharField(max_length=450, null=True)),
                ('status', models.CharField(max_length=450, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='txn_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 14, 14, 7, 58, 613374), editable=False, null=True),
        ),
    ]
