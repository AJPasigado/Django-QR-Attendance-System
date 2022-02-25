from django.db import models


class Types(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Section(models.Model):
    year_level = models.IntegerField()
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.year_level) + ' - ' + self.name


class Attendance(models.Model):
    last_name = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    middle_initial = models.CharField(max_length=1)
    time_stamp = models.DateTimeField()
    user_type = models.ForeignKey(Types, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ', ' + self.middle_initial + '. '
