from django.db import models
from django.core.validators import int_list_validator
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel

from sentinel.utils.models import Province, City


class Office(TimeStampedModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)
    address = models.TextField(_('address'))
    province = models.ForeignKey(Province, null=True, default=None, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, default=None, on_delete=models.CASCADE)

    postal_code = models.CharField(
        _('postal code'),
        max_length=10,
        validators=[int_list_validator(message="Enter only digits number", code='invalid', allow_negative=False)],
        default='')

    email = models.EmailField(_('email'))
    phone = models.CharField(
        _('phone no.'),
        max_length=30,
        blank=True,
        null=True,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ]
    )

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.name
