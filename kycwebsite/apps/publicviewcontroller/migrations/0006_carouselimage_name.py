# Generated by Django 2.2.4 on 2019-08-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("publicviewcontroller", "0005_carouselimage")]

    operations = [
        migrations.AddField(
            model_name="carouselimage",
            name="name",
            field=models.CharField(default="name", max_length=100),
        )
    ]
