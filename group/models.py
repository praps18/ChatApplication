from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('normal', 'Normal User'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='normal')
    


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_groups')
    

    def __str__(self):
        return self.name

    

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes=models.PositiveBigIntegerField(default=0)
    class Meta:
        ordering=('created_date',)


