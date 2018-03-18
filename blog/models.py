from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.BinaryField()
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
''''''
# This will change to blog_post
class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Abstract Class
class blog_post(models.Model):
    blog_post_id = models.AutoField(primary_key=True)
    # The users username should be inserted here
    author = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    text = models.TextField(blank=True)
    user_id = models.ForeignKey('auth.User')

class top_post(blog_post):
    title = models.CharField(max_length=100)

class response_post(blog_post):
    top_post_id = models.ForeignKey('top_post', on_delete=models.PROTECT)

class tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=25)
    blog_post_id = models.ForeignKey('blog_post', on_delete=models.CASCADE)

class image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.BinaryField()
    blog_post_id = models.ForeignKey('blog_post', on_delete=models.CASCADE)

class alerts(models.Model):
    alert_id = models.AutoField(primary_key=True)
    alert_name = models.CharField(max_length=128)

class user_alerts(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_id = models.ForeignKey(alerts, on_delete=models.CASCADE)
