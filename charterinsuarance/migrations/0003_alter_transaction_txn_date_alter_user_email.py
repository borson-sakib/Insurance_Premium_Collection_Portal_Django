# Generated by Django 4.0.4 on 2022-06-30 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charterinsuarance', '0002_user_is_admin_alter_transaction_txn_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='txn_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 30, 16, 11, 46, 699556), editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
