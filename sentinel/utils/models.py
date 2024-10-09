from model_utils.models import TimeStampedModel
from django.db import models
from django.utils.translation import ugettext as _


class Province(models.Model):
    name = models.CharField(max_length=35)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name


class City(models.Model):
    name = models.CharField(max_length=35)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _('cities')
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Confirmation(TimeStampedModel):
    confirm = models.BooleanField(_('data confirm'), default=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.created
