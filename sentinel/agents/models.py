from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, int_list_validator
from django.urls import reverse
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel
from model_utils import Choices

from sentinel.utils.models import Province, City
from sentinel.core.models import Office

AGENT_CODE_STARTING_INDEX = 98600000


class Agent(TimeStampedModel):
    GENDER_CHOICES = Choices(('M', _('Male')), ('F', _('Female')))
    POSITION_CHOICES = Choices(
        ('finconsultant', _('Financial Consultant')), ('manager', _('Manager')), ('director', _('Director')))

    full_name = models.CharField(_('full name'), max_length=100)
    national_id_card_no = models.CharField(
        _('national id card no'),
        max_length=30,
        validators=[
            int_list_validator(
                message="Enter only digits number",
                code='invalid',
                allow_negative=False),
            MaxLengthValidator(16),
            MinLengthValidator(16)
        ],
        null=True)
    place_of_birth = models.CharField(_('place of birth'), max_length=50)
    date_of_birth = models.DateField(_('date of birth'))
    gender = models.CharField(_('gender'), max_length=5, choices=GENDER_CHOICES, default=GENDER_CHOICES.M)
    phone = models.CharField(
        _('phone no.'),
        max_length=30,
        blank=True,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ]
    )
    mobile1 = models.CharField(
        _('primary mobile no.'),
        max_length=30,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ]
    )
    mobile2 = models.CharField(
        _('secondary mobile no.'),
        max_length=30,
        blank=True,
        null=True,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ]
    )

    address = models.TextField(_('address'))
    province = models.ForeignKey(Province, null=True, default=None, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, default=None, on_delete=models.CASCADE)

    postal_code = models.CharField(
        _('postal code'),
        max_length=10,
        validators=[int_list_validator(message="Enter only digits number", code='invalid', allow_negative=False)],
        default='')

    email = models.EmailField(_('email'))

    bank_acc_name = models.CharField(_('bank account name'), max_length=50)
    bank_name = models.CharField(_('bank name'), max_length=50)
    bank_branch = models.CharField(_('bank branch'), max_length=50)
    bank_acc_no = models.CharField(
        _('bank account no.'),
        max_length=30,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ]
    )

    tax_id_no = models.CharField(
        _('tax id no.'),
        max_length=30,
        blank=True
    )
    position = models.CharField(
        _('position'), max_length=50, choices=POSITION_CHOICES, default=POSITION_CHOICES.finconsultant)

    office_location = models.ForeignKey(Office, null=True, default=None, on_delete=models.CASCADE)
    code = models.CharField(_('agents code'), max_length=30, unique=True)

    recruiter = models.ForeignKey('self', related_name='agentrecruiter', blank=True, null=True, default=None, on_delete=models.CASCADE)

    direct_leader = models.ForeignKey('self', blank=True, null=True, related_name='directleader', on_delete=models.CASCADE)
    agency_director = models.ForeignKey('self', blank=True, null=True, related_name='agencydirector', on_delete=models.CASCADE)
    sad_or_rm = models.ForeignKey('self', blank=True, null=True, related_name='sadrms', on_delete=models.CASCADE)

    created_place = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=30, blank=True, null=True)

    photo = models.ImageField(_('photo'), blank=False, upload_to="agents/photos/", default='')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('agents:detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.pk:
            latest_agent = Agent.objects.order_by('-code').first()
            if latest_agent and latest_agent.code:
                self.code = int(latest_agent.code) + 1
            else:
                self.code = AGENT_CODE_STARTING_INDEX
        super(Agent, self).save(*args, **kwargs)
