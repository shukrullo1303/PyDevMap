from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar      = models.FileField(upload_to='avatars/', null=True, blank=True)
    # Sertifikat olganidan keyin True bo'ladi — ism/familiya o'zgartirib bo'lmaydi
    name_locked = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"Profile({self.user.username})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
