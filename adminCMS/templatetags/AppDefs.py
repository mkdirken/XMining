from django import template
from app.models import *
from random import randint

def random_olustur():
    return randint(11111,99999)


register = template.Library()


@register.simple_tag()
def istatistik_cek(par):
    if par=="kasa":
        Kasa=Bank.objects.raw("SELECT id,SUM(pay) as kazanc FROM app_bank WHERE islem=%s",["GİRDİ"])
        if Kasa[0].kazanc is not None:
            return Kasa[0].kazanc
        else:
            return "0"
    elif par=="payment":
        bildiri=Payment.objects.filter(status=False)
        return bildiri.count()

    else:
        talep=RequestPayment.objects.filter(status=False)
        return talep.count()
