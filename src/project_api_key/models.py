from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.core.cache import cache


class ProjectApiKey(models.Model):
    """
    This is a model to store api keys for projects
    """

    cache_timeout = 30
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    pub_key = models.CharField(max_length=64, editable=False)
    sec_key = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return self.pub_key or "Not created"

    def cache_pass_key(self, key: str):
        """
        This method is to cache the unhashed pass key
        """
        cache.set(self.pub_key, key, timeout=self.cache_timeout)

    def get_cached_pass_key(self) -> str:
        """
        This method is to get the unhashed sec_key
        """
        return cache.get(self.pub_key)

    def set_sec_key(self, key: str):
        """
        This method is to set the hashed sec_key
        """
        self.sec_key = make_password(key)

    def check_password(self, sec_key):
        return check_password(sec_key, self.sec_key)

    def is_active(self):
        """
        This method is to check if the user is active
        """
        return self.user.is_active

    def is_staff(self):
        """
        This method is to check if the user is staff
        """
        return (self.user.staff or self.user.admin) and self.is_active()

    class Meta:
        verbose_name = "Api key"
        verbose_name_plural = "Api keys"


@receiver(post_save, sender=ProjectApiKey)
def create_project_api(sender, instance, created, **kwargs):
    if created:
        # Generate random pub_key and pass
        pub_key = get_random_string(16)
        pass_key = f"{get_random_string(6)}.{get_random_string(32)}.{get_random_string(16)}"  # noqa

        instance.pub_key = pub_key
        instance.set_sec_key(pass_key)

        # Cache the pass_key
        instance.cache_pass_key(pass_key)

        instance.save()
