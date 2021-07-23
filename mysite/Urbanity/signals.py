from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# @receiver(post_save, sender=Customer)
# def post_save_generate_otp(sender, instance, created, *args, **kwargs):
#     # if created:
#         instance.otp = random.randint(1000, 9999)
