import json , requests , time , os , re , json
from rich import print_json
from OneClick import Hunter
hd = str(Hunter.Services())
from uuid import uuid4
ud = str(uuid4())
from user_agent import generate_user_agent
gd = str(generate_user_agent())
addlist=[]
addlist2=[]
addlist3=[]
def A_Gmail(email):
    url = 'https://android.clients.google.com/setup/checkavail'
    headers = {
        'Content-Length':'98',
		'Content-Type':'text/plain; charset=UTF-8',
		'Host':'android.clients.google.com',
		'Connection':'Keep-Alive',
		'user-agent':'GoogleLoginService/1.3(m0 JSS15J)',
    }
    data = json.dumps({
        'username':f'{email}',
		'version':'3',
		'firstName':'Aegos',
		'lastName':'Codeing'
    })
    response = requests.post(url,headers=headers,data=data)
    if response.json()['status'] == 'SUCCESS':
        return {'Status':'Available','AEGOS':'@G_4_2'}
    else:
        return {'Status':'UnAvailable','AEGOS':'@G_4_2'}
def A_Yahoo(email):
    email2 = email.split('@')[0]
    url2 = "https://login.yahoo.com/account/module/create?validateField=userId" 
    headers2 = {
	 'accept': '*/*',
	 'accept-encoding': 'gzip, deflate, br',
	 'accept-language': 'en-US,en;q=0.9',
	 'content-length': '7979',
	 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'cookie': 'A1=d=AQABBKsqRWQCEP0UsV5c9lOx8e5im2YNQ50FEgEBAQF8RmRPZAAAAAAA_eMAAA&S=AQAAApW5iPsgjBo-EVpzITncq1w; A3=d=AQABBKsqRWQCEP0UsV5c9lOx8e5im2YNQ50FEgEBAQF8RmRPZAAAAAAA_eMAAA&S=AQAAApW5iPsgjBo-EVpzITncq1w; A1S=d=AQABBKsqRWQCEP0UsV5c9lOx8e5im2YNQ50FEgEBAQF8RmRPZAAAAAAA_eMAAA&S=AQAAApW5iPsgjBo-EVpzITncq1w&j=WORLD; cmp=t=1682254514&j=0&u=1---; B=9qgodcpi4aalb&b=3&s=7t; GUC=AQEBAQFkRnxkT0IiCATl; AS=v=1&s=yWa5asCx&d=A64467c3b|dcjw_0n.2SoXBbaywfJ6pOKLuxGKrtyyLsUqPKnDloZ4PzLBcZineGWbyj4SSiaHVn.6gkyCaIlqSJGryRwnshefN43hbdPocziZnuN6cUMiC9Ls7jght5ak90PZbx8rt9nghZTUPpDYSsMNpii5aA9xWBEhMq__TTmv.rfLHzlCE8rgi5dk5PJouLBujcieRBtI7i.7PwU1jFkaeDhxE4dRMjpAQrjJKc6XqfbTBc5K9QaF6r1YVIVWHEpNrUzbZ_7sSzQ5QFoQNwVBgRzaFtm48hiQlg6S.xsMMdDWkw5xtlG7GZUC.V2jgWNgLScSwqCU_3ntveI_BrcuBy_XAXWQsUzNv3grKBv3qzhOMH3pl8DgTDV3wOo.GqdTtcsaaUn7O0i1hSoA0_EqNIXvRBBdePtBAjPWFZt6sK1Dy8S.kVvW9rIWxonS8GYw6jAw3FrkvM_xk8gxU4oKX1pk3h4m0iJVDQhlr0OOLGW7vBxnzYqidDFi01xQe608kLkJO9qx2X1Xv6XORvYJTNAOVfOMWV83D75M_7L4FOjog8f8F5EkOTU7LymG8GTXY2g4K1xBfGHyzAOPDv9NMjc0I_7wLdATcbn2axvwj5I2xiSqrxK8DYnqTVGqEt.tusj07ij4sobwY0FePNGjLOHICdau9tCajCSqBxtly23flz3iYPQ22Va6uuSaQ.c9mtXsBd0NTlWvlOc6zRdQK.uYkiCYg719UyeIFzDDWeFvQCbuBrstwX.zAkYz2YPaTs8ZGpogdgQ5OhaduuhR5jzvz2mmHXGh5fJ1kxfeClXFWbvCdu3T77mmXHxLGQpr3UZKnmiPO7VjxJoEd9SjYA_NFz9HPbvimmWgmv0DIXvdNvHKCQMYEUROQlk5XIH7oiQ1BtywZNvoWv1D7Q--~A',
	 'origin': 'https://login.yahoo.com',
	 'referer': 'https://login.yahoo.com/account/create?.lang=en-US&src=homepage&activity=ybar-signin&pspid=2023538075&.done=https%3A%2F%2Fwww.yahoo.com%2F&specId=yidregsimplified&done=https%3A%2F%2Fwww.yahoo.com%2F',
	 'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
	 'sec-ch-ua-mobile': '?0',
	 'sec-ch-ua-platform': '"Windows"',
	 'sec-fetch-dest': 'empty',
	 'sec-fetch-mode': 'cors',
	 'sec-fetch-site': 'same-origin',
	 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
	 'x-requested-with': 'XMLHttpRequest',
    }
    data2 = {
	 'specId': 'yidregsimplified',
	 'cacheStored': '',
	 'crumb': 'hrxAgkAZ5jX',
	 'acrumb': 'yWa5asCx',
	 'sessionIndex': '',
	 'done': 'https://www.yahoo.com/',
	 'googleIdToken': '',
	 'authCode': '',
	 'attrSetIndex': '0',
	 'multiDomain': '',
	 'tos0': 'oath_freereg|xa|en-JO',
	 'firstName': 'Aegos',
	 'lastName': 'coding', 
	 'userid-domain': 'yahoo',
	 'userId': f'{email2}',
	 'password': 'szdxfefdgfh',
	 'birthYear': '1998',
	 'signup': '',
    }
    response2 = requests.post(url2,headers=headers2,data=data2).text
    if '{"errors":[]}' in response2:
        return {'Status':'Available','AEGOS':'@G_4_2'}
    else:
        return {'Status':'UnAvailable','AEGOS':'@G_4_2'}
def A_Hotmail(email):
    url3 = f'https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=0&emailAddress={email}&_=1604288577990'
    headers3 = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
    response3 = requests.post(url3, headers=headers3).text
    if 'Neither' in response3:
        return {'Status':'Available','AEGOS':'@G_4_2'}
    else:
        return {'Status':'UnAvailable','AEGOS':'@G_4_2'}
def A_Aol(email):
    email3 = email.split('@')[0]
    url4 = "https://login.aol.com/account/module/create?validateField=yid"
    headers4 = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '18430',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'A1=d=AQABBAcaP2MCEDS0lcVAC7jDxca1x2QPSMAFEgEBAQFrQGNIYwAAAAAA_eMAAA&S=AQAAAk66bvBpHLzQZ0n3bQV7x6U; A3=d=AQABBAcaP2MCEDS0lcVAC7jDxca1x2QPSMAFEgEBAQFrQGNIYwAAAAAA_eMAAA&S=AQAAAk66bvBpHLzQZ0n3bQV7x6U; cmp=t=1665079824&j=0&u=1---; rxx=5dmbu5em0gs.2w52y1t9&v=1; AS=v=1&s=mE9oz2RU&d=A6340990f|BfPo7D7.2Soeua6Q5.JcZFuTeKDZd.VEwARWGa18pr8Nw39Pbg3lrVe2yFRyh3RRePi__A4A5bs6jgblICTjtwR23Xn2FaKNd3g4n2Nyoe0HUPOPhxc2_MkgSPb3Uv64NNH6b4oIbh0d6GPjVX.u1iE75NeNGVgDykpoV.GJb.ZOyA1hi3D079flz5FnGN3UPl4Jos.LGJjKE5jeRFZVRbTJyV_q0zmHwp0WmwaGpmtr2bKK2pVY_9dMpw5J1u9Wx0e_QeNBnAgpvDP_E02PBbuxEQQXAX0GF8IM_gu2g5D1CEPA15ailOgAaPTMDY7plQgXdP3cYarpT20WB0vRVdZXqvfsh7E.m8mX5QyFisDObrlDfLbh6nPbmjU_8BIyAHLvCBoCmF0u4BhXftXCqUgW5SadK6EzXKbn394dWjCdO0YJRStGJo_POkob5FNOWud6u3MY1IZS2ov3OD9LIoJy7w.mSCLZ.M84QgA0UgsGTrDOgTQJWeetwKIYy1RbR8lxFZr0IDwTLBAGflJkaNvnQqWxWbEjftCTvXH2CPXFaCRUnSObHQ2cP1Mb8kro2zkXtaUGmW_cD9oHxidsx6vaOfx4f_fSysGP5Aaa2z6NndXHWh_ium8B45ejj4MFh3F7my8_04UX4WjjiZIqGG0fXcLQxFrB1GY6Vnqo47oSmh4yBcZPV7eQ0CKATeJLshzj2SovAZcIdV1ptsKk9P.LVCZl6MeDskIxd5L6iixeCU6PMq84tz7Gmg6S~A; A1S=d=AQABBAcaP2MCEDS0lcVAC7jDxca1x2QPSMAFEgEBAQFrQGNIYwAAAAAA_eMAAA&S=AQAAAk66bvBpHLzQZ0n3bQV7x6U&j=WORLD',
        'origin': 'https://login.aol.com',
        'referer': 'https://login.aol.com/account/create?intl=uk&lang=en-gb&specId=yidReg&done=https%3A%2F%2Fwww.aol.com',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data4 = {
        'specId': 'yidreg',
        'cacheStored': '',
        'crumb': 'ks78hCqM4K.',
        'acrumb': 'mE9oz2RU',
        'done': 'https://www.aol.com',
        'googleIdToken': '',
        'authCode': '',
        'attrSetIndex': '0',
        'tos0': 'oath_freereg|uk|en-GB',
        'firstName': 'Aegos',
        'lastName': 'Coodeing',
        'yid': email3,
        'password': '1#$aegos$#1wjdytesre',
        'shortCountryCode': 'IQ',
        'phone': '7716555876',
        'mm': '11',
        'dd': '1',
        'yyyy': '1998',
        'freeformGender': '',
        'signup': '',
    }
    response4 = requests.post(url4,headers=headers4,data=data4).text
    if ('{"errors":[]}') in response4:
        return {'Status':'Available','AEGOS':'@G_4_2'}
    else:
        return {'Status':'UnAvailable','AEGOS':'@G_4_2'}
def A_MailRu(email):
    url5 = 'https://account.mail.ru/api/v1/user/exists'
    headers5 = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    data5 = {
'email': str(email)
    }
    response5 = requests.post(url5,headers=headers5,data=data5).text
    if 'exists":false' in response5:
        return {'Status':'Available','AEGOS':'@G_4_2'}
    else:
        return {'Status':'UnAvailable','AEGOS':'@G_4_2'}
def CheckTik(email):
    url = "https://api2-19-h2.musical.ly/aweme/v1/passport/find-password-via-email/?app_language=ar&manifest_version_code=2018101933&_rticket=1656747775754&iid=7115676682581247750&channel=googleplay&language=ar&fp=&device_type=SM-A022F&resolution=720*1471&openudid=8c05dec470c7b7d5&update_version_code=2018101933&sys_region=IQ&os_api=30&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=280&carrier_region=IQ&ac=wifi&device_id=7023349253125604869&mcc_mnc=41805&timezone_offset=10800&os_version=11&version_code=880&carrier_region_v2=418&app_name=musical_ly&ab_version=8.8.0&version_name=8.8.0&device_brand=samsung&ssmix=a&pass-region=1&build_number=8.8.0&device_platform=android&region=SA&aid=1233&ts=1656747775&as=a1e67fbb4fffb246cf0244&cp=f2f02d6bfbffb36de1eomw&mas=01cd120efcb179ac1b331e5cecb80282052c2c4c0c66c66c2c4c46"
    headers = {
            'host':'api2-19-h2.musical.ly',
            'connection':'keep-alive',
            'cookie':'sstore-idc=maliva; store-country-co de=iq; odin_tt=056f31c10f8c82638f6d4d64669ad49e9c36d4946d5d596f433d7f2d75fa1592a21c201d712196d54ee4ae4e14ac8708eee32dc97c85c0a65510024ecc0698346f73ecab038b7160dbff96ced716b8af',
            'accept-Encoding':'gzip',
            'user-agent':'com.zhiliaoapp.musically/2018101933 (Linux; U; Android 11; ar_IQ; SM-A022F; Build/RP1A.200720.012; Cronet/58.0.2991.0)',
            'connection': 'close'        
    }
    data = f"app_language=ar&manifest_version_code=2018101933&_rticket=1656747775754&iid=7115676682581247750&channel=googleplay&language=ar&fp=&device_type=SM-A022F&resolution=720*1471&openudid=8c05dec470c7b7d5&update_version_code=2018101933&sys_region=IQ&os_api=30&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=280&email={email}&retry_type=no_retry&carrier_region=IQ&ac=wifi&device_id=7023349253125604869&mcc_mnc=41805&timezone_offset=10800&os_version=11&version_code=880&carrier_region_v2=418&app_name=musical_ly&ab_version=8.8.0&version_name=8.8.0&device_brand=samsung&ssmix=a&pass-region=1&build_number=8.8.0&device_platform=android&region=SA&aid=1233"
    res = requests.post(url,headers=headers,data=data).text
    if 'Sent successfully' in res:
        return {'Status':'OK','BY':'@G_4_2'}
    else :
        return {'Status':'FALSE','BY':'@G_4_2'}
def CheckInsta(email):
    url2 = 'https://i.instagram.com/api/v1/accounts/login/'
    headers2 = {
        'User-Agent':str(hd),
        'Accept':'*/*',
        'Cookie':'missing',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US',
        'X-IG-Capabilities':'3brTvw==',
        'X-IG-Connection-Type':'WIFI',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'i.instagram.com'        
    }
    data2 = {
        'uuid':ud,
        'password':'Aegos#tele=@F_F_X_F',
        'username':email,
        'device_id':ud,
        'from_reg':'false',
        '_csrftoken':'missing',
        'login_attempt_countn':'0'
    }
    res2 = requests.post(url2,headers=headers2,data=data2).text
    if ('"invalid_user"')in res2:
        return {'Status':'FALSE','BY':'@G_4_2'}
    elif ('"bad_password"') in res2:
        return {'Status':'OK','BY':'@G_4_2'}
    else:
        return {'Status':'FALSE','BY':'@G_4_2'}
def GetInfoTik(user):
    try:
        resp4 = requests.get(f'https://www.tiktok.com/@{user}').text
        getting = str(resp4.split('"UserModule":')[1]).split('"RecommendUserList"')[0]
        i1 = str(getting.split('id":"')[1]).split('",')[0]
        i2 = str(getting.split('nickname":"')[1]).split('",')[0]
        i3 = str(getting.split('signature":"')[1]).split('",')[0]
        i4 = str(getting.split('region":"')[1]).split('",')[0]
        i5 = str(getting.split('privateAccount":')[1]).split(',"')[0]
        i6 = str(getting.split('followerCount":')[1]).split(',"')[0]
        i7 = str(getting.split('followingCount":')[1]).split(',"')[0]
        i8 = str(getting.split('heart":')[1]).split(',"')[0]
        i9 = str(getting.split('videoCount":')[1]).split(',"')[0]
        return {'result':'true','user':'true','id':i1,'name':i2,'bio':i3,'code-country':i4,'private':i5,'followers':i6,'following':i7,'likes':i8,'video':i9,'By':'@G_4_2'}
    except IndexError :
        return {'result':'false','user':'false','By':'@G_4_2'}
def GetInfoInsta(user):
    try:
        url= f"https://i.instagram.com/api/v1/users/web_profile_info/?username={user}"
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'mid=Y3bGYwALAAHNwaKANMB8QCsRu7VA; ig_did=092BD3C7-0BB2-414B-9F43-3170EAED8778; ig_nrcb=1; shbid=1685054; shbts=1675191368.6684434090; rur=CLN; ig_direct_region_hint=ATN; csrftoken=Wcmc9xB0EWESej9SP16gSpt1nBYAsWs7; ds_user_id=6684434090',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': gd,
            'x-asbd-id': '198387',
            'x-csrftoken': 'Wcmc9xB0EWESej9SP16gSpt1nBYAsWs7',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0g7ECdkTdrXy37TE9AoSnMndccWbB1cqrccYOZSLfcb0pE',
            'x-instagram-ajax': '1006383249',
        }
        r4 = requests.get(url,headers=headers).json()
    except :
        return {'result':'false','user':'false','Tele':'@G_4_2'}
    f1 = str(r4['data']['user']['full_name'])
    f2 = str(r4['data']['user']['id'])
    f3 = str(r4['data']['user']['edge_followed_by']['count'])
    f4 = str(r4['data']['user']['edge_follow']['count'])
    f5 = str(r4['data']['user']['edge_owner_to_timeline_media']['count'])
    r5 = requests.get(f"https://o7aa.pythonanywhere.com/?id={f2}").json()
    r6 = r5['date']
    f6 = int(r6)-1
    try:
        hd5 = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            'Connection': 'Keep-Alive',
            'User-Agent': hd,
            'Accept-Language': 'en-US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': 'AQ==',
	    }
        d5 = {
            'ig_sig_key_version': '4',
            "user_id":f2
	    }
        u5 = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
        r6 = requests.post(u5,headers=hd5,data=d5).json()
        f7 = r6['obfuscated_email']
        return {'result':'true','user':'true','name':f1,'id':f2,'followers':f3,'following':f4,'posts':f5,'date':f6,'reset':f7,'Tele':'@G_4_2'}
    except KeyError:
        return {'result':'true','user':'true','name':f1,'id':f2,'followers':f3,'following':f4,'posts':f5,'date':f6,'reset':'false','Tele':'@G_4_2'}