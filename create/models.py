from django.db import models
from member.models import Members


# Create your models here.

class FinalAllShifts(models.Model):

    class Meta(object):
        db_table = 'final_all_shifts'
        unique_together = ('year', 'month', 'day')

    year = models.IntegerField(verbose_name='year', blank=False)
    month = models.IntegerField(verbose_name='month', blank=False)
    day = models.IntegerField(verbose_name='day', blank=False)
    smg_shifts = models.ForeignKey(
        'FinalSmgShifts',
        verbose_name='smg_shifts',
        on_delete=models.CASCADE
    )
    counter_shifts = models.ForeignKey(
        'FinalCounterShifts',
        verbose_name='counter_shifts',
        on_delete=models.CASCADE
    )
    kitchen_shifts = models.ForeignKey(
        'FinalKitchenShifts',
        verbose_name='kitchen_shifts',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)

    # def __str__(self):
    #     return self.year


class FinalSmgShifts(models.Model):

    class Meta(object):
        db_table = 'final_smg_shifts'

    open_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='open_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='open_shifts'
    )
    close_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='close_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='close_shifts'
    )
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)


class FinalCounterShifts(models.Model):
    class Meta(object):
        db_table = 'final_counter_shifts'

    am1_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am1_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_am1_shifts'
    )
    am2_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am2_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_am2_shifts'
    )
    am3_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am3_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_am3_shifts'
    )
    am4_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am4_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_am4_shifts'
    )
    am5_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am5_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_am5_shifts'
    )
    pm1_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm1_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_pm1_shifts'
    )
    pm2_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm2_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_pm2_shifts'
    )
    pm3_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm3_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_pm3_shifts'
    )
    pm4_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm4_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_pm4_shifts'
    )
    pm5_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm5_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='counter_pm5_shifts'
    )
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)


class FinalKitchenShifts(models.Model):
    class Meta(object):
        db_table = 'final_kitchen_shifts'

    am1_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am1_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_am1_shifts'
    )
    am2_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am2_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_am2_shifts'
    )
    am3_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am3_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_am3_shifts'
    )
    am4_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='am4_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_am4_shifts'
    )
    pm1_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm1_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_pm1_shifts'
    )
    pm2_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm2_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_pm2_shifts'
    )
    pm3_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm3_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_pm3_shifts'
    )
    pm4_shifts = models.ForeignKey(
        'FinalPersonalShifts',
        verbose_name='pm4_shifts',
        on_delete=models.CASCADE,
        null=True,
        related_name='kitchen_pm4_shifts'
    )
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)


class FinalPersonalShifts(models.Model):
    class Meta(object):
        db_table = 'final_personal_shifts'

    member = models.ForeignKey(Members, verbose_name='member', on_delete=models.CASCADE)
    since = models.IntegerField(verbose_name='since', blank=False)
    to = models.IntegerField(verbose_name='to', blank=False)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)

    def __str__(self):
        return self.member.name
