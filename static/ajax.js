$('.ceptel').mask('(000) 000 0000');
function login(device) {
    if(device=="mobil"){
        var data=$("#oturum_ac_formu2").serialize();
    }else{
        var data=$("#oturum_ac_formu").serialize();
    }
    document.getElementById("giris_buton1").disabled=true;
    document.getElementById("giris_buton2").disabled=true;
    $.ajax({
        url:"/ajax/login",
        data:data,
        type:"POST",
        dataType:"JSON",
        success:function (cevap) {
            if(cevap.durum==1){
                // Giriş Başarılı
                document.location.href="/app/";
            }else{
                // Hatalı Giriş
                var mesaj="";
                   for(var i in cevap.mesaj){
                        mesaj+=cevap.mesaj[i];
                        mesaj+='<br>';
                    }
                    swal ("",  mesaj ,  "error" );
                // HATALI GİRİŞ OLDUĞU İÇİN BUTONLARIN KILIDINI AÇALIM
                document.getElementById("giris_buton1").disabled=false;
                document.getElementById("giris_buton2").disabled=false;
            }

        }
    })

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


})


function register() {
    var data=$("#kayit_ol_form").serialize();
    $.ajax({
        url:"/ajax/register",
        data:data,
        beforeSend:function () {
             document.getElementById("kayit_ol_buton").disabled=true;
        },complete:function () {
            document.getElementById("kayit_ol_buton").disabled=false;
        }
    })
}