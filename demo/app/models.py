from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
    when_added = models.DateTimeField(auto_now_add=True)
