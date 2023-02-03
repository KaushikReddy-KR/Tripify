from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class S(models.Model):
    objects = models.Manager()
    source = models.CharField(max_length=200)

    def __str__(self):
        return str(self.source)

class D(models.Model):
    objects = models.Manager()
    dest = models.CharField(max_length=200)

    def __str__(self):
        return str(self.dest)


class Journey(models.Model):
    objects = models.Manager()
    pname = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(S, on_delete=models.SET_NULL, null=True, related_name='sources')
    dest = models.ForeignKey(D, on_delete=models.SET_NULL, null=True, related_name='destinations')
    d_date = models.CharField(max_length=200)

    # class Meta:
    #     ordering = ['-updated', '-created']

    def __str__(self):
        return str(self.pname)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message

