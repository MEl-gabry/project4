from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from . import timezone

now = timezone.get_localtime(datetime.now())

class User(AbstractUser):
    followers = models.ManyToManyField('User', blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    text = models.CharField(max_length=1000, validators=[MinLengthValidator(4)])
    date = models.DateTimeField(default=now)
    likers = models.ManyToManyField(User, default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "date": self.date,
            "likers": [liker.username for liker in self.likers.all()]
        }

    def isValid(self):
        return self.text != "" and self.user is not None and self.likers.count() >= 0 