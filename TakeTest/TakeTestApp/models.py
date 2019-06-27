from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField


class Users(User):
    pass


class Tests(models.Model):
    test_name = models.CharField(blank=False, max_length=20)
    test_file = models.FileField(upload_to='uploads/', blank=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False)
    creation_date = models.DateTimeField(auto_now=True, blank=False)
    start_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=24)
    exam_duration = models.IntegerField(default=60)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True)


class Results(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, blank=False)
    score = models.IntegerField(blank=False)
    answers = JSONField()

    class Meta:
        unique_together = ('user', 'test',)
