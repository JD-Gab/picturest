from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class userPictures(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(blank=True, max_length=150)
    description = models.CharField(max_length=900, blank=True)
    upload_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uploader.username + " - " + self.title

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    banner_picture = models.ImageField(upload_to='banner_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class bookmarkImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(userPictures, on_delete=models.CASCADE, related_name='bookmark')
    bookmarked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " - " + self.image.title


