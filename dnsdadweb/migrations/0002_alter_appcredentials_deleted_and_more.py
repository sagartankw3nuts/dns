# Generated by Django 5.0 on 2024-02-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnsdadweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appcredentials',
            name='deleted',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='appcredentials',
            name='redirect_uris',
            field=models.TextField(default=None, null=True),
        ),
    ]
