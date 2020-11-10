from django.db import models


class Class(models.Model):
    student = models.CharField(max_length=30)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=30)
    topic = models.CharField(max_length=60)
    homework = models.CharField(max_length=60, default='None')
    brought_over = models.CharField(max_length=60, default='No')
    remarks = models.CharField(max_length=100, default="None")
    duration = models.FloatField()
    payout = models.IntegerField()

    def __str__(self):
        return f" {self.student} / {self.date} / {self.start_time} / {self.subject}"
