from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    higher_studies = models.BooleanField(default=False)

    def __str__(self):
        return self.username