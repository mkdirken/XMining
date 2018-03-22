from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from random import randint

def random_olustur():
    return randint(11111,99999)

class User(AbstractUser):
    avatar=models.ImageField(default=None,verbose_name="Profil Fotoğrafı",upload_to="users")
    hesap=models.FloatField(default=0,verbose_name="Hesap")
    tel=models.CharField(max_length=20,verbose_name="Cep Telefonu",default="(000) 000 00 00")
    tc_no=models.CharField(max_length=11,verbose_name="T.C Kimlik Numarası",default="00000000000")
    bankName=models.CharField(max_length=50,verbose_name="Banka Adı",default="",blank=True)
    iban=models.CharField(max_length=40,verbose_name="İban No",default="",blank=True)
    code=models.CharField(max_length=5,verbose_name="Code",default=random_olustur,blank=True)
    code_active_date=models.DateTimeField(default=timezone.now,verbose_name="Kodun Geçerlilik Süresi",blank=True)
class machine(models.Model):
    hash_rates=(
        ('TH','TH/s'),
        ('GH','GH/s'),
        ('MH','MH/s')
    )
    warranty_option=(
        ('3 AY','3 AY'),
        ('6 AY','6 AY'),
        ('9 AY','9 AY'),
        ('12 AY','12 AY'),
        ('18 AY','18 AY'),
        ('24 AY','24 AY')
    )
    LifeTime_option=(
        (1,'1 YIL'),
        (2,'2 YIL')
    )
    image=models.ImageField(verbose_name="Görsel",upload_to="machine")
    model=models.CharField(verbose_name="Model",max_length=50)
    properties=models.TextField(verbose_name="Özellikler")
    fiyat=models.FloatField(verbose_name="Fiyat")
    miner_power=models.FloatField(verbose_name="Kazım Gücü")
    miner_power_rate=models.CharField(max_length=10,verbose_name="Kazım Güç Türü",choices=hash_rates)
    warranty=models.CharField(max_length=25,verbose_name="Garanti Süresi",choices=warranty_option)
    lifetime=models.IntegerField(verbose_name="Kullanım Ömrü",choices=LifeTime_option)
    active=models.BooleanField(verbose_name="Aktif/Pasif",default=0)
    class Meta:
        verbose_name = "Yeni Makine Oluştur"
        verbose_name_plural="Yeni Makine Oluştur"

    def __str__(self):
        return self.model


class user_machine(models.Model):
    hash_rates = (
        ('TH','TH/s'),
        ('GH','GH/s'),
        ('MH','MH/s')
    )
    user=models.ForeignKey(User,on_delete=False,related_name="usermachine")
    machine=models.ForeignKey(machine,on_delete=False)
    date=models.DateTimeField(verbose_name="Makine Alım Zamanı")
    machine_dead=models.DateTimeField(verbose_name="Makine Ölüm Zamanı")
    miner_power=models.FloatField(verbose_name="Kazım Gücü")
    miner_power_rate = models.CharField(max_length=10,verbose_name="Kazım Güç Türü",choices=hash_rates)
    fiyat=models.FloatField(verbose_name="Fiyat")
    active=models.BooleanField(verbose_name="Cihaz Aktifliği",default=0)

    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name="Kullanıcıya Ait Cihazlar"
        verbose_name_plural="Kullanıcıya Ait Cihazlar"

class user_machine_log(models.Model):
    user_machine=models.ForeignKey(user_machine,on_delete=False)
    user=models.ForeignKey(User,on_delete=False)
    machine_id=models.IntegerField(verbose_name="Makine ID")
    date=models.DateTimeField()
    machine_dead=models.DateTimeField(default=timezone.now,verbose_name="Makina Ölüm Zamanı")
    pay=models.FloatField(default=0,verbose_name="Kazanç")
    payment=models.BooleanField(default=False,verbose_name="Ödeme Yapıldımı")

class TheMachineGain(models.Model):
    machine=models.ForeignKey(machine,on_delete=False,verbose_name="Makina Modeli")
    gain=models.FloatField(verbose_name="Kazanç")
    date=models.DateField(verbose_name="Zaman")
    class Meta:
        verbose_name = "Makinelerın Günlük Kazancı"
        verbose_name_plural="Makinelerın Günlük Kazancı"


class news(models.Model):
    title=models.CharField(verbose_name="Başlık",max_length=200)
    post=models.TextField(verbose_name="Kısa Yazı")
    date=models.DateTimeField(auto_now_add=True,verbose_name="Zaman")
    class Meta:
        verbose_name = "Duyuru Oluştur"
        verbose_name_plural="Duyuru Oluştur"

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=False)
    fullname=models.CharField(verbose_name="İsim",max_length=120,blank=True)
    bankname=models.CharField(verbose_name="Banka Adı",max_length=60,blank=True)
    iban=models.CharField(verbose_name="İban No",max_length=40,blank=True)
    amount=models.IntegerField(verbose_name="Tutar",default=0)
    cellphone=models.CharField(max_length=20,verbose_name="Telefon Numarası",blank=True)
    date=models.DateTimeField(default=timezone.now,verbose_name="Bildirim Gönderim Zamanı")
    status=models.BooleanField(verbose_name="Ödeme Durumu",default=False)

    class Meta:
        verbose_name = "Gelen Ödeme Bildirimleri"
        verbose_name_plural="Gelen Ödeme Bildirimleri"


class RequestPayment(models.Model):
    user=models.ForeignKey(User,on_delete=False)
    fullname=models.CharField(verbose_name="İsim",max_length=120,blank=True)
    bankName=models.CharField(verbose_name="Banka Adı",max_length=60,blank=True)
    iban=models.CharField(verbose_name="İban No",max_length=40,blank=True)
    amount=models.IntegerField(verbose_name="Tutar",default=0)
    date=models.DateTimeField(default=timezone.now,verbose_name="Talep Tarihi")
    status=models.BooleanField(verbose_name="Ödeme Durumu",default=False)

    class Meta:
        verbose_name="İstenen Ödeme Talebi"
        verbose_name_plural="İstenen Ödeme Talebi"



class Bank(models.Model):
    islem_turu=(
        ("GİRDİ","GİRDİ"),
        ("ÇIKTI","ÇIKTI")
    )
    user=models.ForeignKey(User,on_delete=False)
    title=models.CharField(verbose_name="İşlem",max_length=100,default="Girilmemiş")
    date=models.DateField(verbose_name="İşlem Tarihi",default=timezone.now)
    pay=models.FloatField(verbose_name="Ödeme",default=0)
    islem=models.CharField(max_length=20,verbose_name="İşlem Türü",default="GİRDİ",choices=islem_turu)

    class Meta:
        verbose_name="Kasa"
        verbose_name_plural = "Kasa"

class Investment(models.Model):
    user=models.ForeignKey(User,on_delete=False)
    pay=models.IntegerField(verbose_name="Yatırım Tutarı",default=0)
    date=models.DateTimeField(auto_now_add=True,verbose_name="Yatırım Zamanı")
    status=models.BooleanField(verbose_name="Hesaba Aktarma",default=False)
