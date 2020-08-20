from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profil')
    image = models.ImageField(upload_to='img/picture', default='profile.jpg')

    def __str__(self):
        return self.user.username