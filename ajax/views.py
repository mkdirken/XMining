from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login as dj_login,authenticate
from app.forms import *
import json
import requests
import datetime
from django.contrib.auth.hashers import check_password
from api.defs import *
from random import randint

def random_olustur():
    return randint(11111,99999)


def borsa_cek(request):
    r = requests.get('http://bitfindeks.com/rest/ticker/apiV1')
    if r.status_code==200:
        borsa=r.json()
        eth=borsa[13]["coinRate"]
        btc=borsa[17]["coinRate"]
        ltc=borsa[26]["coinRate"]
        xrp=borsa[72]["coinRate"]
        return HttpResponse(json.dumps({'allborsa':borsa,'eth':eth,'btc':btc,'ltc':ltc,'xrp':xrp}),content_type="application/json")
    else:
        return HttpResponse(json.dumps({'allborsa':0,'eth':0,'btc':0,'ltc':0,'xrp':0}),content_type="application/json")




def login(request):
    if request.is_ajax():
        form=LoginForm(request.POST or None)
        if form.is_valid():
            ## Giriş Başarılı Oturumu başlatalım
            dj_login(request,form.user)
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')

def register(request):
    if request.is_ajax():
        form = Register( request.POST or None)
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate( request,username=username,password=password)
            ## Giriş Başarılı Oturumu başlatalım
            dj_login(request,new_user)
            return HttpResponse(json.dumps({ 'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum': 0,'mesaj': form.errors}),content_type="application/json")
    else:
        return redirect( 'home')

def update_user(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdateUserForm(request.POST or None,instance=request.user)
        if form.is_valid():
            update=form.save(commit=False)
            update.user=request.user
            update.save()
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')
def cep_update(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdateCepForm(request.POST or None,user=request.user)
        if form.is_valid():
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')

def update_password(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdatePasswordForm(request.POST or None,user=request.user)
        if form.is_valid():
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')

def update_avatar(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdateAvatarForm(request.POST or None, request.FILES or None,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')


def MachineBuy(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=MachineBuyForm(request.POST or None,user=request.user)
        if form.is_valid():
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')

def payment(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=PaymentForm(request.POST or None,user=request.user)
        if form.is_valid():
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')


def request_payment(request):
    if request.is_ajax() and request.user.is_authenticated:
        simdiki_zaman = timezone.now()
        kod_active = request.user.code_active_date
        if simdiki_zaman > kod_active:
            return HttpResponse(json.dumps({'durum': 2,'mesaj': "Onay Kodun Süresi Dolmuş Tekrar Kod İsteyin"}),content_type="application/json")
        else:
            form=RequestPaymentForm(request.POST or None,user=request.user)
            if form.is_valid():
                return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')



def request_code(request):
    if request.user.is_authenticated:
        simdiki_zaman=timezone.now()
        kod_active=request.user.code_active_date
        if simdiki_zaman>kod_active:
            # Kodun Geçerlilik Süresi Dolmuş
            ## kodu oluşturup kullanıcaya mesajını atalım
            request.user.code_active_date=simdiki_zaman+datetime.timedelta(minutes=3)
            random_kod=random_olustur()
            request.user.code=random_kod
            request.user.save()
            ## Kullanıcaya Kodunu mesaj atalım
            icerik='BitfindeksMining Onay Kodunuz : '+str(random_kod)
            mesaj=send_sms(icerik,request.user.tel)
            if mesaj==False:
                return HttpResponse(json.dumps({'durum': 0,'mesaj': 'Kod Gönderilemedi'}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'durum': 1,'mesaj': 'Kod Gönderildi gelen kodu kod alanına yazın'}),content_type="application/json")

        else:
            # Kodun Geçerlilik Süresi Devam Ediyor
            return HttpResponse(json.dumps({'durum': 2,'mesaj': 'Gönderilen Kodun Geçerlilik Süresi Devam Ediyor!'}),content_type="application/json")
    else:
        return redirect('home')