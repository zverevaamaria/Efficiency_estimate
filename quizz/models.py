from django.db import models

class ProjectInfo(models.Model):

    longesity = models.IntegerField()
    discount_type = models.CharField(max_length=30)
    discount_rate = models.IntegerField()
    npv = models.FloatField()
    irr = models.IntegerField()
    pi = models.IntegerField()


    def __str__(self):
        return self.discount_type# Create your models here.
