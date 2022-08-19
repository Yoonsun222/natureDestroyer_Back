from django.db import models

# Create your models here.
class User(models.Model):
    school = models.CharField(max_length = 20, null = False)
    nickname = models.CharField(max_length = 20, null = False)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nickname

class Ranking(models.Model):
    school = models.CharField(max_length = 20, null = False)
    best = models.CharField(max_length = 20, null = False)
    trash = models.CharField(max_length = 20, null = False)
    avg_score = models.IntegerField(default=0)
    def __str__(self):
        return self.school
     