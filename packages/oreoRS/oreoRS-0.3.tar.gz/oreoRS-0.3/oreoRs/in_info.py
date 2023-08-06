import requests
from OneClick import Hunter
hf = str(Hunter.Services())
def InfoRS(user):
    url = f'https://lookup.socialservicesapi.com/api/user/username/{user}?api_key=e8451c0868bac19b75f2c405d34eb67b'
    res = requests.get(url).json()
    qq = res['id']
    ww = res['username']
    ee = res['biography']
    rr = res['full_name']
    tt = res['followers']
    yy = res['following']
    hh = requests.get(f"https://o7aa.pythonanywhere.com/?id={qq}").json()
    mm = hh['date']
    try:
        hd5 = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            'Connection': 'Keep-Alive',
            'User-Agent': hf,
            'Accept-Language': 'en-US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': 'AQ==',
	    }
        d5 = {
            'ig_sig_key_version': '4',
            "user_id":qq
	    }
        u5 = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        r6 = requests.post(u5,headers=hd5,data=d5).json()
        h7 = r6['obfuscated_email']
        return {'status':'true','name':rr,'id':qq,'followers':tt,'following':yy,'date':mm,'reset':h7,'By':'@X_6_Z'}
    except KeyError:
        return {'status':'true','name':rr,'id':qq,'followers':tt,'following':yy,'date':mm,'By':'@X_6_Z'}

