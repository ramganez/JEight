from django.db import models

from datetime import datetime

# Create your models here.


class CommonInfo(models.Model):
    created_on = models.DateTimeField(default=datetime.now, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class RoomMember(CommonInfo):
    name = models.CharField(max_length=50,)
    mobile = models.CharField(max_length=12,)
    mail_id = models.EmailField(max_length=75,)
    advance_given = models.DecimalField(max_digits=6, decimal_places=2)
    other_exp_paid = models.DecimalField(max_digits=6, decimal_places=2)

    def clean(self):
        """extra whitespace will be stripped"""
        if self.name:
            self.name = self.name.strip()

    def __unicode__(self):
        return self.name


class MonthExpense(CommonInfo):
    rent = models.DecimalField(max_digits=7, decimal_places=2, default=8000)
    maintenance = models.DecimalField(max_digits=7, decimal_places=2,
                                      default=300)
    cable = models.DecimalField(max_digits=7, decimal_places=2, default=150)
    EB = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    water = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    commonEB = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    veg_shop = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    other = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __unicode__(self):
        return self.created_on.strftime('%B')

    def get_total_exp(self):
        return (self.rent + self.maintenance + self.cable +
                self.EB + self.water + self.commonEB + self.veg_shop + self.other)


class MonthInvesment(CommonInfo):
    provision_store = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    new_things = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    gas = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    rice_bag = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __unicode__(self):
        return self.created_on.strftime('%B')

    def get_total_inves(self):
        return (self.provision_store + self.new_things +
                self.gas + self.rice_bag)


class AdjustmentFromPeople(CommonInfo):
    fk_invesment = models.ForeignKey(MonthInvesment)
    people_name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)


class IndividualShare(CommonInfo):
    fk_room_member = models.OneToOneField(RoomMember, unique=True)
    fk_afp = models.ForeignKey(AdjustmentFromPeople, blank=True, null=True)
    shared = models.CharField(max_length=10, default='All')
    amount_to_pay = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __unicode__(self):
        return "month_share: %s" % self.fk_room_member.name
