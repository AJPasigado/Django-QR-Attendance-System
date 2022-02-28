from django.db import models


class Types(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Types, self).save(*args, **kwargs)


class Section(models.Model):
    year_level = models.IntegerField()
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.year_level) + ' - ' + self.name

    @property
    def section_name(self):
        return str(self.year_level) + ' - ' + self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Section, self).save(*args, **kwargs)


class Attendance(models.Model):
    last_name = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    middle_initial = models.CharField(max_length=1)
    time_stamp = models.DateTimeField()
    user_type = models.ForeignKey(Types, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ', ' + self.middle_initial + '. '

    def save(self, *args, **kwargs):
        self.middle_initial = self.middle_initial.title()
        super(Attendance, self).save(*args, **kwargs)
