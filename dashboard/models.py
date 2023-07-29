from django.db import models
from django.contrib.auth.models import User, Group
from django_countries.fields import CountryField

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = CountryField(max_length=2)
    rib = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} - Subscription"

subscribre_group, created = Group.objects.get_or_create(name='Subscriber')
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', default='user.png')

    def __str__(self):
        return self.user.username
