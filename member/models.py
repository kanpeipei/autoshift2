from django.db import models

# Create your models here.


class Members(models.Model):

    class Meta(object):
        db_table = 'members'

    name = models.CharField(verbose_name='name', max_length=255)
    age = models.IntegerField(verbose_name='age')
    partner_number = models.IntegerField(verbose_name='partner_number', blank=False, unique=True)
    hourly_pay = models.IntegerField(verbose_name='hourly_pay')
    is_counter = models.BooleanField(verbose_name='is_counter')
    is_fryer = models.BooleanField(verbose_name='is_fryer')
    is_kitchen = models.BooleanField(verbose_name='is_kitchen')
    is_smg = models.BooleanField(verbose_name='is_smg')
    is_opener = models.BooleanField(verbose_name='is_opener')
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at', auto_now=True)

    def __str__(self):
        return self.name
