from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=20)
    grade = models.CharField(max_length=20, blank=True)
    school = models.CharField(max_length=20, blank=True)
    subjects = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    hourly_rate = models.IntegerField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=20)
    base_rate = models.IntegerField()

    def __str__(self):
        return self.name



