from _csv import list_dialects
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User,machine,TheMachineGain,news,Payment,Bank,RequestPayment,user_machine


class musteriler(UserAdmin):
    list_display =['username','first_name','last_name','email','tel','hesap']
    list_display_links = ['username','first_name','last_name','email','tel','hesap']
    search_fields = ['username','tel']
    class Meta:
        model=User


class cihaz_ekle(admin.ModelAdmin):
    list_display = ['model','fiyat','miner_power','active']
    list_display_links = ['model','fiyat','miner_power','active']
    search_fields = ['model']
    def has_delete_permission(self, request, obj=None):
        return False
    class Meta:
        model=machine


class gunluk_tutar(admin.ModelAdmin):
    list_display = ['date','machine','gain']
    list_display_links = ['date','machine','gain']
    list_filter = ['date']
    search_fields = ['date']
    class Meta:
        model=TheMachineGain

class duyurular(admin.ModelAdmin):
    list_display =['title','date']
    list_display_links = ['title','date']
    list_filter = ['date']
    search_fields = ['date']
    class Meta:
        model=news

class odeme_bildirim(admin.ModelAdmin):
    list_display = ['fullname','cellphone','date']
    list_display_links = ['fullname', 'cellphone', 'date']
    search_fields = ['date','fullname','cellphone']
    class Meta:
        model=Payment


class kasa(admin.ModelAdmin):
    list_display =['user','date','islem']
    list_display_links = ['user','date','islem']
    search_fields=['date']
    def has_delete_permission(self, request, obj=None):
        return False
    class Meta:
        model=Bank

class odeme_istegi(admin.ModelAdmin):
    list_display = ['fullname','bankName','date','status']
    list_display_links = ['fullname','bankName','date','status']
    search_fields = ['date','fullname']
    def has_delete_permission(self, request, obj=None):
        return False
    class Meta:
        model=RequestPayment

class kullanici_cihazlar(admin.ModelAdmin):
    list_display = ['user','machine','date','active']
    list_display_links = ['user','machine','date','active']
    search_fields = ['user_id']

    def has_delete_permission(self, request, obj=None):
        return False

    class Meta:
        model=user_machine

admin.site.register(User,musteriler)
admin.site.register(machine,cihaz_ekle)
admin.site.register(TheMachineGain,gunluk_tutar)
admin.site.register(news,duyurular)
admin.site.register(Payment,odeme_bildirim)
admin.site.register(Bank,kasa)
admin.site.register(RequestPayment,odeme_istegi)
admin.site.register(user_machine,kullanici_cihazlar)

admin.site.site_header='Coinet Admin Paneli'
admin.site.site_title="Bitfindeks Mining"
