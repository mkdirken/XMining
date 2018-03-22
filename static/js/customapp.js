$('.cep_tel').mask('(000) 000 00 00');
$('.iban').mask('TR00 0000 0000 0000 0000 00');
window.onload = function(e){
     loading_close();
}
function loading() {
    $(".loader").fadeIn("slow");
}
function loading_close() {
     $(".loader").fadeOut("slow");
}
function formatMyMoney(price) {
  var currency_symbol = "₺"

  var formattedOutput = new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
      minimumFractionDigits: 2,
    });

  return formattedOutput.format(price).replace(currency_symbol, '')+" ₺"
}
function mesajlar(par) {
     var mesaj="";
       for(var i in par){
            mesaj+=par[i];
            mesaj+='\n';
        }
        swal ("",  mesaj ,  "error" );
}
$(function () {

    // AJAX AYARLARI
   $.ajaxSetup({
      type:"POST",
      dataType:"JSON",
      success:function (cevap) {
            if(cevap.durum==1){
                document.location.reload();
            }else{
               mesajlar(cevap.mesaj);
            }
        },error:function () {
            swal ("TimeOut",  "" ,  "error" );
            document.location.reload();
        }
    });

   // BORSA BİLGİLERİNİ ÇEK
    borsa_cek();

    // MARKET FİYATLARINI MASKELE
    market_fiyatlarini_maskele();

    // TL MASKELE
    $('.tl-maskla').each(function () {
        var para=$(this).text();
        para=para.replace(',','.');
        $(this).text(formatMyMoney(parseFloat(para)));
    })

    // DATATABLELERİ OLUŞTUR
    $('#tablo1').DataTable();
    $('#tablo2').DataTable();
    $('#tablo3').DataTable();
    $('#tablo4').DataTable();
    $('#tablo5').DataTable();
})

// USER
// PROFILI GUNCELLE
function user_update() {
    var data=$("#update_user_form").serialize();
    $.ajax({
        url:"/ajax/update_user",
        data:data,
        beforeSend:function () {
             document.getElementById("profil_guncelle_buton").disabled=true;
            loading();
        },
        complete:function () {
            loading_close();
            document.getElementById("profil_guncelle_buton").disabled=false;
        }
    })
}
function update_password() {
    var data=$("#update_password_form").serialize();
    $.ajax({
        url:"/ajax/update_password",
        data:data,
        beforeSend:function () {
             document.getElementById("sifre_guncelle_buton").disabled=true;
            loading();
        },complete:function () {
            loading_close();
            document.getElementById("sifre_guncelle_buton").disabled=false;
        }
    })
}
function cep_guncelle() {
    var data=$("#cep_guncelle_form").serialize();
    $.ajax({
        url:"/ajax/cep_update",
        data:data,
        beforeSend:function () {
             document.getElementById("cep_guncelle_buton").disabled=true;
            loading();
        },complete:function () {
            loading_close();
            document.getElementById("cep_guncelle_buton").disabled=false;
        }
    })
}
function change_avatar() {
    $.ajax({
        url:"/ajax/update_avatar",
        data:new FormData(document.getElementById("change_avatar_form")),
        contentType: false,
        cache: false,
        processData:false,
    })

}


// SON USER


// BORSA
// BORSA BİLGİLERİNİ ÇEK
function borsa_cek() {
    $.ajax({
        url:"/ajax/borsa",
        type:"GET",
        beforeSend:function () {
        },
        complete:function () {

        },success:function (cevap) {
            document.getElementById("btc").innerHTML=formatMyMoney(cevap.btc);
            document.getElementById("xrp").innerHTML=formatMyMoney(cevap.xrp);
            document.getElementById("ltc").innerHTML=formatMyMoney(cevap.ltc);
            document.getElementById("eth").innerHTML=formatMyMoney(cevap.eth);

            hesap=$("#hesap").attr('hesap');
            document.getElementById("hesaptobtc").innerHTML=(parseFloat(hesap)/parseFloat(cevap.btc)).toFixed(8)+"...";
        }
    })
}

// SON BORSA


// MARKET
    function market_fiyatlarini_maskele() {
        $(".machine_fiyat").each(function () {
            fiyat=parseFloat($(this).text());
           $(this).text(formatMyMoney(fiyat));
        })
    }
    function satin_al(thiss,id) {
        var fiyat=$(thiss).attr("fiyat");
        var model=$(thiss).attr("name");
        var csrfmiddlewaretoken=$('input[name="csrfmiddlewaretoken"]').val();

        swal({
          title: model,
          text: model+" Model Cihazı "+fiyat+"₺'ye Almak İstiyor musunuz ?",
          icon: "warning",
          buttons: ["Hayır!", "SATIN AL!"],
        }).then((yanit) => {
          if (yanit) {
              $.ajax({
                 url:"/ajax/machinebuy",
                  data:{'csrfmiddlewaretoken':csrfmiddlewaretoken,'machineid':id},
                  beforeSend:function () {
                         $('.satin_al_buton').attr("disabled", true);
                        loading();
                  },complete:function () {
                        loading_close();
                        $('.satin_al_buton').attr("disabled", false);
                    },
                  success:function (cevap) {
                        if(cevap.durum==1){
                            document.location.href="/app/store";
                        }else{
                           mesajlar(cevap.mesaj);
                        }
                    }
              });
            }
        });


    }
// SON MARKET


// ÖDEME
    function odeme_bildir() {
        var data=$('#odeme_bildiri_formu').serialize();
        $.ajax({
            url:'/ajax/payment',
            data:data,
            beforeSend:function () {
                 document.getElementById("odeme_bildiri_buton").disabled=true;
                loading();
            },complete:function () {
                loading_close();
            },success:function (cevap) {
                if(cevap.durum==1){
                    swal("Ödeme Bildirimi Talebiniz Gönderildi", "", "success");
                    document.getElementById("odeme_bildiri_buton").remove();
                }else{
                   mesajlar(cevap.mesaj)
                   document.getElementById("odeme_bildiri_buton").disabled=false;
                }
            }
        })
    }

    function odeme_iste() {
        var data=$('#odeme_talep_formu').serialize();
        $.ajax({
            url:'/ajax/request_payment',
            data:data,
            beforeSend:function () {
                 document.getElementById("odeme_iste_buton").disabled=true;
                loading();
            },complete:function () {
                loading_close();
            },success:function (cevap) {
                if(cevap.durum==1){
                    swal("Ödeme İsteği Talebiniz Gönderildi", "", "success");
                    document.getElementById("odeme_iste_buton").remove();
                }else if(cevap.durum==2){
                    document.getElementById("odeme_iste_buton").disabled=false;
                    swal(cevap.mesaj, "", "warning");
                }else{
                   mesajlar(cevap.mesaj)
                   document.getElementById("odeme_iste_buton").disabled=false;
                }
            }
        })
    }

function request_code() {
    $.ajax({
        type:"GET",
        url:"/ajax/request_code",
        datatype:"JSON",
        beforeSend:function () {
             document.getElementById("request_code").disabled=true;
            loading();
        },complete:function () {
            document.getElementById("request_code").disabled=false;
            loading_close();
        },success:function (cevap) {

            $(".code_mesaj").text(cevap.mesaj);
        }
    })
}
// SON ÖDEME


// MASK
function rakamKontrol(olay){
	var tusKodu;
	if(window.event){ // IE
		tusKodu = olay.keyCode
	}else if(olay.which){ // Netscape/Firefox/Opera
		tusKodu = olay.which;
	}
	if(tusKodu == 8){ // backspace tuşuna da izin vermek istiyorsak
		return true;
	}
	if (tusKodu < 48 || tusKodu > 57){
	    tusKodu.keyCode = 0;
	    return  false;
	}
	else{
	    return true;
	}
}