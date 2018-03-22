from django import forms
from .models import User,machine,user_machine,user_machine_log,Payment,RequestPayment
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import datetime
from random import randint

def random_olustur():
    return randint(11111,99999)

## FORM İÇİN GEREKLİ ARAÇ FONKSYİONLARI
def AddYear(date, years):
    result = date + datetime.timedelta(366 * years)
    if years > 0:
        while result.year - date.year > years or date.month < result.month or date.day < result.day:
            result += datetime.timedelta(-1)
    elif years < 0:
        while result.year - date.year < years or date.month > result.month or date.day > result.day:
            result += datetime.timedelta(1)
    return result

#######

##############################################################3
## KULLANICI LOGIN FORMU
class LoginForm(forms.ModelForm):
    user=None
    class Meta:
        model=User
        fields=('username','password')
    def clean(self):
        kullanici_adi=self.cleaned_data.get("username")
        sifre=self.cleaned_data.get("password")
        if kullanici_adi and sifre:
            self.user=authenticate(username=kullanici_adi,password=sifre)
            if self.user is None:
                # Kullanıcı adı veya şifre yanlış
                raise forms.ValidationError("Kullanıcı Adı veya Şifre Hatalı !")
        else:
            raise forms.ValidationError("Boş Bırakmayınız !")



##############################################################3
## KAYIT OLMA
class Register(forms.ModelForm):

    class Meta:
        model=User
        fields=[
            'first_name','last_name','tel','email','username','password'
        ]

    password2=forms.CharField(required=False)

    def clean(self):
        username=self.cleaned_data.get('username')
        first_name=self.cleaned_data.get("first_name")
        last_name=self.cleaned_data.get("last_name")
        tel=self.cleaned_data.get("tel")
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")
        password2=self.cleaned_data.get("password2")

        if username and first_name and last_name and tel and email and password and password2:
            if password2==password:
                if len(tel)>13:
                    varmi=User.objects.filter(username=username)
                    if varmi.count()>0:
                        raise forms.ValidationError("Kullanıcı Adınız Zaten Sistemde Mevcut")
                else:
                    raise forms.ValidationError("Telefon Numaranızı Doğru Giriniz !")
            else:
                raise forms.ValidationError("Şifreniz Tekrarı İle Uyuşmuyor !")
        else:
            raise forms.ValidationError("İstenilen Tüm Alanları Doldurun !")



##############################################################3
## KULLANICI BİLGİLERİNİ GÜNCELLEME FORMU
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'first_name','last_name','tc_no','email','bankName','iban'
        ]

    def clean(self):
        first_name=self.cleaned_data.get("first_name")
        last_name=self.cleaned_data.get("last_name")
        tel=self.cleaned_data.get("tel")
        tc_no=self.cleaned_data.get("tc_no")
        email=self.cleaned_data.get("email")
        bankName=self.cleaned_data.get("bankName")
        iban=self.cleaned_data.get("iban")

        if first_name and last_name  and tc_no and email:
            pass
        else:
            raise forms.ValidationError("İstenilen Tüm Alanları Doldurun !")



##############################################################3
## KULLANICI CEP GÜNCELLEME FORMU
class UpdateCepForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(UpdateCepForm, self).__init__(*args,**kwargs)

    class Meta:
        model=User
        fields=[
            'tel'
        ]

    code=forms.CharField(max_length=5,required=False)

    def clean(self):
        tel=self.cleaned_data.get('tel')
        code=self.cleaned_data.get('code')
        if timezone.now()<self.user.code_active_date:
            if code==self.user.code:
                if tel and code:
                    if len(tel)>14:
                        if self.user.tel!=tel:
                            self.user.tel=tel
                            self.user.save()
                        else:
                            raise forms.ValidationError("Eski Telefon Numaranız Yenisi İle Aynı!")
                    else:
                        raise forms.ValidationError("Yanlış Telefon Numarası Girdiniz")

                else:
                    raise forms.ValidationError("Yeni Telefonunuzu ve Onay Kodunu Boş Bırakmayın !")
            else:
                raise forms.ValidationError("Onay Kodunu Yanlış Girdiniz !")
        else:
            raise forms.ValidationError("Onay Kodunuzun Süresi Dolmuş Tekrar İsteyin !")



##############################################################3
### KULLANICI ŞİFRE DEĞİŞTİRME FORMU
class UpdatePasswordForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(UpdatePasswordForm, self).__init__(*args,**kwargs)
    new_password=forms.CharField(max_length=40,required=False)
    new_password2=forms.CharField(max_length=40,required=False)
    class Meta:
        model=User
        fields=[
            'password'
        ]

    def clean(self):
        new_password=self.cleaned_data.get("new_password")
        new_password2=self.cleaned_data.get("new_password2")
        password=self.cleaned_data.get("password")
        if new_password and new_password2 and password:
            if new_password!=new_password2:
                raise forms.ValidationError("Yeni Şifreniz Tekrarı İle Uyuşmuyor")
            else:
                if not self.user.check_password(password):
                    raise forms.ValidationError("Şifrenizi Yanlış Girdiniz !")
                else:
                    self.user.set_password(new_password)
                    self.user.save()
        else:
            raise forms.ValidationError("Tüm Alanları Doldurun !")

##############################################################3
## KULLANICI FOTOĞRAF DEĞİŞTİRME FORMU
class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'avatar'
        ]


##############################################################3
## CİHAZ SATIN ALMA FORMU
class MachineBuyForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(MachineBuyForm, self).__init__(*args,**kwargs)

    machineid=forms.IntegerField(required=False)

    def clean(self):
        MachineId=self.cleaned_data.get('machineid')
        ## Bu makina Varmı kontol edelim
        Mac=machine.objects.filter(id=MachineId)
        print ("POST :",MachineId)
        if Mac:
            ## MACHİNE MEVCUT
            ## BAKİYE KONTROL
            if self.user.hesap>Mac[0].fiyat:
                ## BAKİYE VAR BAKİYEDEN EKSİLTİP CİHAZI SATIN ALALIM
                self.user.hesap=self.user.hesap-Mac[0].fiyat
                self.user.save()
                ## BAKİYEDEN DÜŞTÜK ŞİMDİ KULLANICIIN MAKİNELER TABLOSUNA VE LOG TABLOSUNA BUNLARI EKLEYEK
                UserMac=user_machine()
                UserMac.fiyat=Mac[0].fiyat
                UserMac.user_id=self.user.id
                UserMac.machine_id=Mac[0].id
                UserMac.miner_power=Mac[0].miner_power
                UserMac.miner_power_rate=Mac[0].miner_power_rate
                birhafta=(timezone.now()+datetime.timedelta(weeks=1))
                UserMac.date=birhafta
                machine_dead=AddYear((timezone.now()+datetime.timedelta(weeks=1)),Mac[0].lifetime)
                UserMac.machine_dead=machine_dead
                UserMac.save()
                ## Kullanının Makinesi Tanımlandı Şimdi loga atalım
                UserMacLog = user_machine_log()
                UserMacLog.machine_id = Mac[ 0].id
                UserMacLog.user_machine_id = UserMac.id
                UserMacLog.date = birhafta
                UserMacLog.machine_dead = machine_dead
                UserMacLog.user_id = self.user.id
                UserMacLog.save()
            else:
                ## BAKİYE YOK
                raise forms.ValidationError("Bakiyeniz Yeterli Değil Lütfen Yükleme Yapın !")
        else:
            raise forms.ValidationError("Cihaz Mevcut Değil Kaldırılmış Olabilir !")


#########################################################################
# ÖDEME BİLDİRİMİ FORMU
class PaymentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(PaymentForm, self).__init__(*args,**kwargs)

    class Meta:
        model=Payment
        fields=[
            'fullname','bankname','iban','amount','cellphone'
        ]

    def clean(self):
        fullname=self.cleaned_data.get('fullname')
        bankname=self.cleaned_data.get('bankname')
        iban=self.cleaned_data.get('iban')
        amount=self.cleaned_data.get('amount')
        cellphone=self.cleaned_data.get('cellphone')

        if fullname and bankname and iban and amount and cellphone:
            if len(cellphone)>14:
                ## İstenilen Bilgiler Doğru Bildirimi Oluşturalım
                Pay=Payment()
                Pay.user_id=self.user.id
                Pay.fullname=fullname
                Pay.bankname=bankname
                Pay.iban=iban
                Pay.amount=amount
                Pay.cellphone=cellphone
                Pay.save()
                ## Kayıt Oluşturuldu
            else:
                ## Telefon Numarası Yanlış
                raise forms.ValidationError("Telefon Numarasını Doğru Giriniz")
        else:
            ## İSTENİLEN ALANLAR BOŞ
            raise forms.ValidationError("İstenilen Tüm Alanları Doldurun !")


#########################################################################
# ÖDEME TALEP FORMU
class RequestPaymentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(RequestPaymentForm, self).__init__(*args,**kwargs)

    code=forms.CharField(max_length=10,required=False)
    class Meta:
        model=RequestPayment
        fields=[
            'fullname','bankName','iban','amount'
        ]

    def clean(self):
        fullname=self.cleaned_data.get('fullname')
        bankName=self.cleaned_data.get('bankName')
        iban=self.cleaned_data.get('iban')
        amount=self.cleaned_data.get('amount')
        code=self.cleaned_data.get('code')
        if fullname and bankName and iban and amount and code:
            ## KOD KONTROL
            if code==self.user.code:
                ## DAHA ÖNCEDEN GÖNDERMİŞ VE ÖDENMEMİŞ TALEP VARMI
                PayCount=RequestPayment.objects.raw("SELECT id,COUNT(id) as toplam FROM  app_requestpayment WHERE status=%s AND user_id=%s",[False,self.user.id])
                if PayCount[0].toplam==0:
                    ## İSTENİLEN FİYATI HESAPTAN DÜŞELİM
                    self.user.hesap=float(self.user.hesap)-float(amount)
                    self.user.save()
                     ## İstenilen Bilgiler Doğru Bildirimi Oluşturalım
                    Pay=RequestPayment()
                    Pay.user_id=self.user.id
                    Pay.fullname=fullname
                    Pay.bankName=bankName
                    Pay.iban=iban
                    Pay.amount=amount
                    Pay.save()
                    ## Kayıt Oluşturuldu
                else:
                    raise forms.ValidationError("Sırada Ödenecek Bir İstediğiniz Zaten Mevcut")
            else:
                raise forms.ValidationError("Onay Kodunu Yanlış Girdiniz")
        else:
            ## İSTENİLEN ALANLAR BOŞ
            raise forms.ValidationError("İstenilen Tüm Alanları Doldurun !")