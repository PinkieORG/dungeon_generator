from django.db import models


class Dungeon(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content
