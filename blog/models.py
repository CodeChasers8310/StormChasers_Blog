from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class profile(models.Model):
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profileImages/%Y/%m/%d/%H/%M/%S/%f')
    zip = models.IntegerField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    # Not in data model
    is_storm_spotter = models.BooleanField(default=False)

# This is supposed to speed up querying users - but also breaks the model...
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''

class top_post(models.Model):
    post_id = models.AutoField(primary_key=True, default=None)
    title = models.CharField(max_length=100)
    # The users username should be inserted here
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True)
    user_id = models.ForeignKey('auth.User', default=None)

class response_post(models.Model):
    post_id = models.AutoField(primary_key=True)
    top_post_id = models.ForeignKey('top_post', on_delete=models.PROTECT)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(blank=True)
    user_id = models.ForeignKey('auth.User', default=None)
    top_post_id = models.ForeignKey('top_post')

class tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=25)
    top_post_id = models.ForeignKey('top_post', on_delete=models.CASCADE, blank=True, default=None)
    response_post_id = models.ForeignKey('response_post', on_delete=models.CASCADE, blank=True, default=None)

class image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='blogImages/%Y/%m/%d')
    top_post_id = models.ForeignKey('top_post', on_delete=models.CASCADE)

class alerts(models.Model):
    alert_id = models.AutoField(primary_key=True)
    alert_name = models.CharField(max_length=128)

class user_alerts(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    alert_id = models.ForeignKey(alerts, on_delete=models.CASCADE)
