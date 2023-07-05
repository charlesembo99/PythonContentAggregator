from django.db import models

# Create your models here.
class Episode(models.Model):
    title=models.CharField(max_length=255)
    description = models.TextField()
    episode_url = models.URLField()
    thumbnail = models.ImageField()
    postcast_name=models.CharField(max_length=255)
    guide=models.CharField(max_length=55)

    def __str__(self) -> str:
        return f'{self.postcast_name}: {self.title}'
    
    