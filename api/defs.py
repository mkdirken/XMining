import httplib2
import json

def send_sms(message, phones):

  sms_msg = {
    'username' : '##########', # https://oim.verimor.com.tr/sms_settings/edit adresinden öğrenebilirsiniz.
    'password' : '###########', # https://oim.verimor.com.tr/sms_settings/edit adresinden belirlemeniz gerekir.
    'source_addr' : "##########", # Gönderici başlığı, https://oim.verimor.com.tr/headers adresinde onaylanmış olmalı, değilse 400 hatası alırsınız.
    'messages' : [
      {'msg': message, 'dest': phones}
    ]
  }

  sms_msg = json.dumps(sms_msg)
  conn = httplib2.Http()
  request_headers = {'Content-type': 'application/json'}
  response,content=conn.request(uri="http://sms.verimor.com.tr/v2/send.json",method="POST",headers=request_headers,body=sms_msg)
  print(response.status, response.reason)
  if response.status == 200:
    return True
  else:
    return False
