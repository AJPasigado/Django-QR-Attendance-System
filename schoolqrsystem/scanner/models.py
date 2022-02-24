from django.db import models


class Attendance(models.Model):
    student_id = models.IntegerField()
    last_name = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    middle_initial = models.CharField(max_length=1)
    time_stamp = models.DateTimeField()

    def __str__(self):
        return self.time_stamp
