# Generated by Django 3.1.4 on 2020-12-27 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_accounts_mobile_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='cookie',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
