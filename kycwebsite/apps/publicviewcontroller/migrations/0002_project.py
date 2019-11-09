# Generated by Django 2.2.1 on 2019-07-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("publicviewcontroller", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("project_name", models.CharField(max_length=100)),
                ("display", models.BooleanField(default=True)),
                ("hours", models.DecimalField(decimal_places=2, max_digits=4)),
                ("members_attended", models.IntegerField(default=0)),
                ("date", models.DateField(verbose_name="Event Date")),
            ],
        )
    ]
