from django.db import models
from member.models import Members

# Create your models here.


class RequestedShifts(models.Model):

    class Meta(object):
        db_table = 'requested_shifts'
        unique_together = ('member', 'year', 'month', 'day')

    member = models.ForeignKey(Members, verbose_name='member', on_delete=models.CASCADE)
    year = models.IntegerField(verbose_name='year', blank=False)
    month = models.IntegerField(verbose_name='month', blank=False)
    day = models.IntegerField(verbose_name='day', blank=False)
    is_absence = models.BooleanField(verbose_name='is_absence', default=False)
    since = models.IntegerField(verbose_name='since', default=9, blank=False)
    to = models.IntegerField(verbose_name='to', default=22, blank=False)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)

    def __str__(self):
        return self.member.name
