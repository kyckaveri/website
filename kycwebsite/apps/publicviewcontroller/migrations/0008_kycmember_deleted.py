# Generated by Django 2.2.4 on 2019-08-24 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("publicviewcontroller", "0007_auto_20190824_1852")]

    operations = [
        migrations.AddField(
            model_name="kycmember",
            name="deleted",
            field=models.BooleanField(default=False),
        )
    ]
