from django.db import models

class Bio(models.Model):
    description = models.TextField()

class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    retire = models.BooleanField()

    bio = models.OneToOneField(Bio, on_delete=models.CASCADE, null=True)
    films = models.ManyToManyField('films.Film', related_name='actors')


