# Generated by Django 4.0.4 on 2022-08-10 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charterinsuarance', '0015_alter_transaction_txn_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='txn_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 10, 17, 49, 12, 173866), editable=False, null=True),
        ),
    ]