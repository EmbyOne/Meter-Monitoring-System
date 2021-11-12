from django.db import models

class Meter(models.Model):
    value = models.PositiveIntegerField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'meter'

class Archive(models.Model):
    value = models.PositiveIntegerField()
    time = models.DateTimeField()

    class Meta:
        db_table = 'archive'
    
class Alert(models.Model):
    #Literally just gonna store the primary key of archive in this.
    tragedy = models.PositiveIntegerField()

