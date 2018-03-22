from django.shortcuts import render,HttpResponse,redirect,render_to_response
from .forms import *
from .models import *
from django.contrib.auth import logout
import datetime
from django.utils import timezone
from django.db import connection


###############################################################
###############################################################
def home(request):
    return render(request,'index.html')

###############################################################
###############################################################
def index(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## KULLANICILARA AİT TÜM İŞLEMLER BU FONKSYİONDA
    user_operations(request)
    ## HABERLERİ ÇEKELİM
    haberler=news.objects.all().order_by('-id')[:4]
    ## KULLANICININ CİHAZLARINI ÇEKELİM
    active_machines=user_machine.objects.raw("SELECT usmac.id,usmac.date,usmac.miner_power,mac.model,mac.image,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s AND usmac.machine_dead>=%s AND usmac.date<%s ",[request.user.id,timezone.now(),timezone.now()])
    pas_machines = user_machine.objects.raw("SELECT usmac.id,usmac.date,usmac.miner_power,mac.model,mac.image,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s AND usmac.machine_dead>=%s AND usmac.date>%s ",[request.user.id, timezone.now(),timezone.now()])
    onarim_machines=user_machine.objects.raw("SELECT usmac.id,usmac.date,usmac.miner_power,mac.model,mac.image,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s AND usmac.machine_dead>=%s AND usmac.date<%s AND usmac.active=%s ",[request.user.id,timezone.now(),timezone.now(), False])
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista=cihaz_istatistik(request)
    context = {
        'link': 'index',
        'haberler':haberler,
        'active_machines':active_machines,
        'pas_machines':pas_machines,
        'onarim_machines':onarim_machines,
        'zaman':timezone.now,
        'cihaz_istatistik':cihaz_ista,
        'active_count':len(list(active_machines)),
        'pas_count':len(list(pas_machines)),
        'onar_count':len(list(onarim_machines)),
    }
    return render(request,'app/index.html',context)

###############################################################
###############################################################
def user(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## UPDATE FORMUNU OLUŞTURALIM
    form=UpdateUserForm(instance=request.user)
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    context={
        'link':'user',
        'form':form,
        'cihaz_istatistik':cihaz_ista
    }
    return  render(request,'app/user.html',context)

###############################################################
###############################################################
def user_logout(request):
    logout(request)
    return redirect('home')

###############################################################
###############################################################
def market(request):
    if not request.user.is_authenticated:
        return redirect('home')
    ## Tüm Makineleri Çağırılam
    machines=machine.objects.raw("SELECT ap.id,ap.image,ap.model,ap.properties,ap.fiyat,ap.miner_power,ap.miner_power_rate,ap.warranty,ap.lifetime,AVG(the.gain) as Ortalama FROM app_machine as ap INNER JOIN app_themachinegain as the on the.machine_id=ap.id GROUP BY ap.id")
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    context={
        'link':'market',
        'machines':machines,
        'cihaz_istatistik':cihaz_ista

    }
    return  render(request,'app/market.html',context)

###############################################################
###############################################################
def store(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## Kullanıcının Tüm Makinelerini Çağıralım
    user_id=request.user.id
    usermachines=User.objects.raw('select usmac.id,usmac.active,usmac.date,usmac.miner_power,usmac.fiyat,usmac.machine_dead,model,user_id,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s',[user_id])
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    zaman=timezone.now()
    context={
        'link':'store',
        'usermachines':usermachines,
        'cihaz_istatistik':cihaz_ista,
        'zaman':zaman
    }
    return render(request,'app/store.html',context)

###############################################################
###############################################################
def report(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    zaman=timezone.now()
    context={
        'link':'report',
        'cihaz_istatistik':cihaz_ista,
        'zaman':zaman
    }
    return render(request,'app/report.html',context)

###############################################################
###############################################################
def log(request):
    if not request.user.is_authenticated:
        return redirect('home')
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    zaman=timezone.now()
    ## GİREN HESAP HAREKETLERİ
    girens=user_machine_log.objects.raw("SELECT mac.model,usmac.pay,usmac.id,usmac.date FROM app_user_machine_log as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.payment=%s AND usmac.user_id=%s",[True,request.user.id])
    ## ÇIKAN HESAP HAREKETLERİ
    cikans=user_machine.objects.raw("SELECT mac.model,usmac.fiyat,usmac.id,usmac.date FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s",[request.user.id])
    cikans2=RequestPayment.objects.filter(user_id=request.user.id)
    ## YATIRIM HAREKERLERİ
    yatirims=Investment.objects.filter(user_id=request.user.id,status=True)
    context={
        'link':'log',
        'cihaz_istatistik':cihaz_ista,
        'zaman':zaman,
        'girens':girens,
        'yatirims':yatirims,
        'cikans':cikans,
        'cikans2':cikans2
    }
    return render(request,'app/log.html',context)


###############################################################
###############################################################
def cihaz_istatistik(request):
    print ("---------",timezone.now())
    rows=request.user.usermachine.all().filter(machine_dead__gte=timezone.now())
    mh=0
    th=0
    gh=0
    makine_count=rows.count
    active_machine=0
    for row in rows:

        if timezone.now()>row.date and row.active==True:
            active_machine+=1
            if row.miner_power_rate=='TH':
                th=float(th)+float(row.miner_power)
            elif row.miner_power_rate=='GH':
                gh= float(gh)+float(row.miner_power)
            else:
                mh=float(mh)+float(row.miner_power)

    thh=float(th)+float(float(gh)/1000)+(float(mh)/1000000)
    ghh=float(gh)+float(float(mh)/1000)+(float(th)*1000)
    mhh=float(mh)+float(float(gh)*1000)+(float(th)*1000000)

    active_hash=ghh
    active_hash_name="AKTİF HASH RATE GH/S"

    if ghh>1000:
        active_hash=thh
        active_hash_name = "AKTİF HASH RATE TH/S"
    elif ghh<1:
        active_hash = mhh
        active_hash_name = "AKTİF HASH RATE MH/S"



    return {'mh':mhh,'th':thh,'gh':ghh,'cihazlar':rows,'makine_count':makine_count,'active_machine':active_machine,'active_hash':active_hash,'active_hash_name':active_hash_name}

###############################################################
###############################################################
def user_operations(request):
    cursor=connection.cursor()

    ## ÖDEME BİLDİRİMİ ONAYLANMIŞSA YATIRIM GELİRİ OLARAK HESABA EKLEYELİM
    yatirim=0
    odeme_bildirimi=Payment.objects.filter(user_id=request.user.id,status=True)
    for i in range(0,len(odeme_bildirimi)):
        yatirim+=odeme_bildirimi[i].amount
        TableYatirim=Investment()
        TableYatirim.user_id=request.user.id
        TableYatirim.pay=odeme_bildirimi[i].amount
        TableYatirim.date=odeme_bildirimi[i].date
        TableYatirim.status=True
        TableYatirim.save()
        cursor.execute("DELETE FROM app_payment WHERE id=%s",[odeme_bildirimi[i].id])
    ## YATIRIM GETİRİLERİNİ HESABA YÜKLEYELİM
    request.user.hesap=request.user.hesap+yatirim
    request.user.save()


    ## KULLANICININ ÖDENMEMİŞ CİHAZLARINI ÇEKELİM
    zaman=timezone.now()-datetime.timedelta(days=1)
    odeme_tutari=0
    UserMac=user_machine_log.objects.filter(date__lte=zaman,payment=False,user_id=request.user.id)
    for i in range(0,len(UserMac)): ## Ödeme Alacak Cihazları dönelim
        gecen_zaman=(timezone.now()-UserMac[i].date).days
        ## GEÇEN ZAMANI LOG KAYITLARINA TEK TEK EKLEYELİM
        for gun in range(0,gecen_zaman):
            # Geçen Zaman Hangi gün ödeme olucak
            odeme_gunu=UserMac[i].date+datetime.timedelta(days=gun)
            TheMachine=TheMachineGain.objects.filter(date__lte=odeme_gunu,machine_id=UserMac[i].machine_id).order_by('-date')[:1]
            para=(TheMachine[0].gain/100)*65
            odeme_tutari=odeme_tutari+para
            kasa_pay=TheMachine[0].gain-para
            ## USERLOG ÖDEMESİ ALINDI GÜNCELLE
            cursor.execute("UPDATE app_user_machine_log SET payment=%s,pay=%s WHERE date=%s AND user_id=%s AND user_machine_id=%s",[True,para,odeme_gunu,request.user.id,UserMac[i].user_machine_id])
            ## USERLOG 1 Gün Sonrasını kayıt edelim
            UserLog=user_machine_log()
            UserLog.date=(odeme_gunu+datetime.timedelta(days=1))
            UserLog.machine_dead=UserMac[i].machine_dead
            UserLog.machine_id=UserMac[i].machine_id
            UserLog.user_id=UserMac[i].user_id
            UserLog.user_machine_id=UserMac[i].user_machine_id
            UserLog.save()
            ## KASAYA İŞLEMİ BELİRTELİM
            kasa=Bank()
            kasa.islem="GİRDİ"
            kasa.pay=kasa_pay
            kasa.date=odeme_gunu
            kasa.title="%35 KULLANICI GELİRİ"
            kasa.user_id=request.user.id
            kasa.save()
    ## HESABA PARASINI YÜKLEYELİM
    request.user.hesap=float(request.user.hesap)+odeme_tutari
    request.user.save()