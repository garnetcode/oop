from django.db import models


class Article(models.Model):
    date = models.DateTimeField(auto_now=True)
    scene = models.ImageField(default='default.jpg', null=True,  upload_to='news/')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    content = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title) + " by " + str(self.author)

