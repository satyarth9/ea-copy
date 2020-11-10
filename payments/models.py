from django.db import models
from home.models import Student


class Payment(models.Model):
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    span = models.CharField(max_length=5)
    amount = models.IntegerField()
    received_datetime = models.DateTimeField()
    mode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student_name} - {self.span} - {self.amount}"
