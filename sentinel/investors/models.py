from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import ugettext as _
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django.core.validators import int_list_validator

from mptt.models import MPTTModel, TreeForeignKey

from sentinel.agents.models import Agent
from sentinel.utils.models import Province, City


TENOR_CHOICES = Choices(
    (3, 'quarter', _('3 Months')),
    (6, 'semester', _('6 Months')),
    (12, 'annual', _('12 Months')),
)


class Investor(TimeStampedModel):

    INVESTOR_TYPE_CHOICES = Choices(('individual', _('Individual')), ('corporate', _('Corporate')))

    financial_consultant = models.ForeignKey(Agent, null=True, on_delete=models.CASCADE)
    investor_type = models.CharField(
        _('investor type'),
        max_length=20,
        choices=INVESTOR_TYPE_CHOICES,
        default=INVESTOR_TYPE_CHOICES.individual)

    name = models.CharField(_('name'), max_length=50)
    pic_corporate = models.CharField(_('Pic name'), max_length=50, blank=True, null=True)
    pic_position = models.CharField(_('Pic position'), max_length=50, blank=True, null=True)

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
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True, default=None)

    address = models.TextField(_('address'))
    province = models.ForeignKey(Province, null=True, default=None, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, default=None, on_delete=models.CASCADE)

    postal_code = models.CharField(
        _('postal code'),
        max_length=10,
        validators=[int_list_validator(message="Enter only digits number", code='invalid', allow_negative=False)],
        default='')

    phone = models.CharField(
        _('phone'),
        max_length=30,
        blank=True,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ]
    )
    mobile1 = models.CharField(
        _('primary mobile no.'),
        max_length=30,
        validators=[int_list_validator(message="Enter only digits number", code='invalid', allow_negative=False)])
    mobile2 = models.CharField(
        _('secondary mobile no.'),
        max_length=30,
        blank=True,
        default='',
        validators=[int_list_validator(message="Enter only digits number", code='invalid', allow_negative=False)])

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
        blank=True,
        null=True,
        default='',
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['created']


class Deposit(MPTTModel, TimeStampedModel):

    DEPOSIT_TYPE_CHOICES = Choices(
        ('netto', _('Netto')),
        ('gross', _('Gross')),
    )

    TRANSACTION_TYPE_CHOICES = Choices(
        ('overbooking', _('Overbooking')),
        ('trans_or_rtgs', _('Transaction or RTGS')),
        ('cheque_or_giro', _('Cheque or Giro No.')),
    )

    PRODUCT_TYPE_CHOICES = Choices(('hypn', _('HYPN')), ('isprint', _('ISPRINT')))

    form_no = models.CharField(
        _('formulir no.'),
        max_length=7,
        unique=True,
        help_text=_('e.x: 1021031')
    )
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)

    deposit_type = models.CharField(
        _('deposit'),
        max_length=10,
        choices=DEPOSIT_TYPE_CHOICES,
        default=DEPOSIT_TYPE_CHOICES.netto)

    amount = models.DecimalField(
        _('amount'),
        max_digits=16,
        decimal_places=2,
        help_text=_('Please input: 150000000')
    )

    transaction_type = models.CharField(
        _('transaction type'),
        max_length=30,
        choices=TRANSACTION_TYPE_CHOICES,
        default=TRANSACTION_TYPE_CHOICES.trans_or_rtgs)

    bank_acc_name = models.CharField(_('bank account name'), max_length=50)
    bank_name = models.CharField(_('bank name'), max_length=50)
    bank_acc_no = models.CharField(
        _('bank account no.'),
        max_length=30,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ],
        null=True
    )

    transaction_date = models.DateField(_('transaction date'))

    invest_tenor = models.PositiveSmallIntegerField(
        _('tenor'),
        choices=TENOR_CHOICES,
        default=TENOR_CHOICES.quarter
    )

    invest_return = models.DecimalField(
        _('return'),
        max_digits=5,
        decimal_places=2,
        help_text=_('Please input: 2.50')
    )

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default=PRODUCT_TYPE_CHOICES.hypn
    )

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    is_ro = models.BooleanField(_('is rollover'), default=False)

    def __unicode__(self):
        return '{} - {}'.format(self.form_no, self.investor.name)

    class Meta:
        ordering = ['created']


class Withdrawal(TimeStampedModel):
    deposit = models.OneToOneField(Deposit, on_delete=models.CASCADE)

    form_no = models.CharField(
        _('formulir no.'),
        max_length=7,
        unique=True,
        help_text=_('e.x: 1021031')
    )
    withdrawal_date = models.DateField(_('withdrawal date'))
    amount = models.DecimalField(
        _('amount'),
        max_digits=16,
        decimal_places=2,
        help_text='Currency in Rp (Rupiah)'
    )
    notes = models.TextField(_('notes'), max_length=100, blank=True)

    bank_acc_name = models.CharField(_('bank account name'), max_length=50)
    bank_name = models.CharField(_('bank name'), max_length=50)
    bank_acc_no = models.CharField(
        _('bank account no.'),
        max_length=30,
        validators=[
            int_list_validator(sep='-', message="Enter only digits number", code='invalid', allow_negative=False)
        ],
    )

    def __unicode__(self):
        return '{} - {}'.format(self.form_no, self.deposit.investor.name)

    class Meta:
        ordering = ['created']
