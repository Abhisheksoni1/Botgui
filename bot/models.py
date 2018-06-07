from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
# from bot.forms import *
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(max_length=1500, default='', blank=True, null=True)

    def __str__(self):
        return self.name

    # class Meta:
        # managed = False
        # verbose_name_plural = 'contact'
        # verbose_name = 'contact'
        # db_table = 'contact'


class EmailSubscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email





# # class Profile(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     email = models.EmailField(default=False)
# #     # phone = models.IntegerField(null=True, blank=True)
# #
# #     def __str__(self):
# #         return self.user.username
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
