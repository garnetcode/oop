from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    picture = models.ImageField(default='default.jpg', null=True,  upload_to='profiles/')
    description = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

# Create your models here.
