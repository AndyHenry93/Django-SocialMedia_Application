from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
123
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField() 
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images',default ='profile-icon.png')
    location = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username