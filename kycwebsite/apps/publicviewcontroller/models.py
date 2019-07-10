from django.db import models


class Position(models.Model):
    """ Lower number (importance) = higher up. -1 is reserved for Adult Coordinator
        importance field is used to sort members """

    importance = models.IntegerField(default=0)
    position_name = models.CharField(max_length=30)

    def __str__(self):
        return self.position_name


class KYCMember(models.Model):
    # TODO: deleting a kyc member throws an error when it shouldn't
    name = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.position.importance - other.position.importance < 0

    def __eq__(self, other):
        return self.position.importance - other.position.importance == 0 and self.name == other.name

    def __gt__(self, other):
        return self.position.importance - other.position.importance > 0


class Project(models.Model):
    """ A KYC Event """

    project_name = models.CharField(max_length=100)
    display = models.BooleanField(default=True)
    hours = models.DecimalField(decimal_places=2, max_digits=4)
    members_attended = models.IntegerField(default=0)
    date = models.DateField('Event Date')
    image_url = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.project_name} - {self.date.month}/{self.date.day}/{self.date.year}"

    def __lt__(self, other):
        return self.date < other.date

    def __eq__(self, other):
        return self.date == other.date

    def __gt__(self, other):
        return self.date > other.date
