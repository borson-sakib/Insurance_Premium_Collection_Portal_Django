# Generated by Django 4.0.4 on 2022-08-10 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charterinsuarance', '0014_rename_branchcode_transaction_branch_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='txn_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 10, 17, 46, 21, 480254), editable=False, null=True),
        ),
    ]
