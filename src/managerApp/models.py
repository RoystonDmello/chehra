from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # for python 2
    def __unicode__(self):
        return self.user.username

    # for python 3
    def __str__(self):
        return self.user.username


'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Teacher.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.teacher.save()

'''

