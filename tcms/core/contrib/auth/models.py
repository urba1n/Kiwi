# -*- coding: utf-8 -*-

import datetime
try:
    import secrets
except ImportError:
    # note: this is *only* because RTD still runs Python 3.5
    # which doesn't have the secrets module. This workaround makes
    # the doc builds pass! If you try using Kiwi TCMS on Python 3.5
    # it will still fail below b/c 'secrets' is not defined!
    pass

from django.db import models
from django.conf import settings


class UserActivateKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=64, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'tcms_user_activate_keys'

    @classmethod
    def set_random_key_for_user(cls, user, force=False):
        activation_key = secrets.token_hex()

        # Create and save their profile
        user_activation_key, created = cls.objects.get_or_create(user=user)
        if created or force:
            user_activation_key.activation_key = activation_key
            user_activation_key.key_expires = datetime.datetime.today() + datetime.timedelta(7)
            user_activation_key.save()

        return user_activation_key
