from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Question(models.Model):
    test = ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    name = models.CharField(max_length=100)


class Answer(models.Model):
    question = ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    name = models.CharField(max_length=50)
    correctness = models.BooleanField(default=False)
