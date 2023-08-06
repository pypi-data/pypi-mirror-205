try:
	from uuid import uuid4
	import uuid
	import random
	import requests
	from user_agent import generate_user_agent
	import os
	import instaloader
	import re
	import json
except ModuleNotFoundError:
	import os
	os.system("pip install instaloader")
	os.system("pip install json")
	os.system("pip install re")
	os.system("pip install user_agent")
	os.system("pip install uuid")
class Zaid:
	def get(user,sessionid):
		L = instaloader.Instaloader()
		profile = str(instaloader.Profile.from_username(L.context,user))
		idd=str(profile.split(')>')[0])
		iid = idd.split(' (')[1]
		url = "https://i.instagram.com/api/v1/users/"+str(iid)+"/info/"
		headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    "cookie": "ig_did=57C594DF-134B-4172-BCF1-C32A7A21989B; mid=X_sqxgALAAE7joUQdF9J2KQUb0bw; ig_nrcb=1; shbid=2205; shbts=1614954604.1671221; fbm_124024574287414=base_domain=.instagram.com; csrftoken=hE6dtVq6z7Zozo4yfyVPOpTJNEktuPky; rur=FRC; ds_user_id=46430696274; sessionid=" + sessionid + "",
	"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
	"sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "none",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36 Instagram 166.1.0.42.245 Android (29/10; 420dpi; 1080x2042; samsung; SM-G973F; beyond1; exynos9820; en_GB; 256099204)"}
		data = ""
		response = requests.Session().get(url, data=data, headers=headers).json()
		if response['user']['is_business'] == True and str(response['user']['public_email']) != "":
			email = str(response['user'].get('public_email'))
			if str("@") in email:
				print(email)
			else:
				return False
		else:
			return False
	

	def Tik_Check(email: str) -> str:
		email = email
		url = 'https://api2-19-h2.musical.ly/aweme/v1/passport/find-password-via-email/?app_language=ar&manifest_version_code=2018101933&_rticket=1667149902064&iid=7160349471136909061&channel=googleplay&language=ar&fp=&device_type=ANY-LX2&resolution=1080*2298&openudid=39e9b96bb5c6e336&update_version_code=2018101933&sys_region=IQ&os_api=30&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=480&carrier_region=IQ&ac=wifi&device_id=7116197109661091333&mcc_mnc=41805&timezone_offset=10800&os_version=11&version_code=880&carrier_region_v2=418&app_name=musical_ly&ab_version=8.8.0&version_name=8.8.0&device_brand=HONOR&ssmix=a&pass-region=1&build_number=8.8.0&device_platform=android&region=SA&aid=1233&ts=1667149902&as=a1261b755ea4d3e04e4388&cp=be4a3c6ce5e8520fe1MkUo&mas=0149d8edb9a3340aacd5c82fcadadde3801c1ccc2ca62c0ca6cc26'
		headers = {
	'Host': 'api2-19-h2.musical.ly',
	'Connection': 'keep-alive',
	'Content-Length': '647',
	'Cookie': 'odin_tt=b0db11ac4955afa4589bdb09d8f8fdcf3bcdea5238d0a6e2ba7c6aaea542e8d4ff9a3f324c153df80e03ac5e29a9d411925fa05d2f300713a2295db1eeff68accf50d5ddb5abd11115077fe989cfc094; store-idc=maliva; store-country-code=iq; store-country-code-src=did',
	'Accept-Encoding': 'gzip',
	'X-SS-QUERIES': 'dGMCAr6ot3awALq2qSjedy1Vk99nIoud%2BAhHSPAsj5dyUWFbxRx0wm95EoKwwNB3VVlOMd4SzMIENA51cwBS%2Bm0N1T95yguPVZ4OunAWAs0t0bHbsPclnVdl1Uh%2BLGZVXFGTew%3D%3D',
	'sdk-version': '1',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-SS-TC': '0',
	'User-Agent': 'com.zhiliaoapp.musically/2018101933 (Linux; U; Android 11; ar_IQ_#u-nu-latn; ANY-LX2; Build/HONORANY-L22CQ; Cronet/58.0.2991.0)'
	}
	
	
		data = (f'app_language=ar&manifest_version_code=2018101933&_rticket=1667150564079&iid=7160349471136909061&channel=googleplay&language=ar&fp=&device_type=ANY-LX2&resolution=1080*2298&openudid=39e9b96bb5c6e336&update_version_code=2018101933&sys_region=IQ&os_api=30&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=480&email={email}&retry_type=no_retry&carrier_region=IQ&ac=wifi&device_id=7116197109661091333&mcc_mnc=41805&timezone_offset=10800&os_version=11&version_code=880&carrier_region_v2=418&app_name=musical_ly&ab_version=8.8.0&version_name=8.8.0&device_brand=HONOR&ssmix=a&pass-region=1&build_number=8.8.0&device_platform=android&region=SA&aid=1233')
		rr = requests.post(url, headers=headers, data=data).text
		if 'Sent successfully' in rr:
			return {"TikTok":"Good","Response ":True}
		else:
			return {"TikTok":"Bad","Response ":False}
			
	def inst_Check(email: str) -> str:
		uid = uuid4()
		url='https://i.instagram.com/api/v1/accounts/login/'
		headers = {'User-Agent':'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',  'Accept':'*/*',
                 'Cookie':'missing',
                 'Accept-Encoding':'gzip, deflate',
                 'Accept-Language':'en-US',
                 'X-IG-Capabilities':'3brTvw==',
                 'X-IG-Connection-Type':'WIFI',
                 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
              'Host':'i.instagram.com'}
		data = {'uuid':uid,  'password':'@zaidforty0',
              'username':email,
              'device_id':uid,
              'from_reg':'false',
              '_csrftoken':'missing',
              'login_attempt_countn':'0'}
		req= requests.post(url, headers=headers, data=data).json()
		if req['message'] == 'The password you entered is incorrect. Please try again.':
			return {"Instagram":"Good","Response ":True}
		else:
			return {"Instagram":"Bad","Response ":False} 
			
	def Token_Face(cookies: str) -> str:
		try:
			r=requests.Session()
			r.headers.update({'referer': 'https://m.facebook.com/',})
			data = r.get('https://business.facebook.com/business_locations', headers = {
							'user-agent'                : 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36', # don't change this user agent.
							'referer'                   : 'https://www.facebook.com/',
							'host'                      : 'business.facebook.com',
							'origin'                    : 'https://business.facebook.com',
							'upgrade-insecure-requests' : '1',
							'accept-language'           : 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
							'cache-control'             : 'max-age=0',
							'accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'content-type'              : 'text/html; charset=utf-8'
						}, cookies = {
							'cookie'                    : cookies
						})
						
						
					
			find_token = re.search('(EAAG\w+)', data.text)
			#print(find_token)
			return '\n* Fail : maybe your cookie invalid !!' if (find_token is None) else find_token.group(1)
			#print(results)
		except requests.exceptions.ConnectionError:
			return '\n* Fail : no connection here !!'
		except:
		    return '\n* Fail : unknown errors, please try again !!'
		    

	def Login_Face(user,pw):
			ses=requests.Session()
			application_version = str(random.randint(111,555))+'.0.0.'+str(random.randrange(9,49))+str(random.randint(111,555))
			application_version_code=str(random.randint(000000000,999999999))
			fbs=random.choice(['com.facebook.adsmanager','com.facebook.lite','com.facebook.orca','com.facebook.katana','com.facebook.mlite'])
			gtt=random.choice(['GT-I9190','KOT49H','GT-I9192','KOT49H','GT-I9300I','KTU84P','GT-I9300','IMM76D','GT-I9300','JSS15J','GT-I9301I','KOT4','GT-I9301I','KOT49H','GT-I9500','JDQ39','GT-I9500','LRX22C','GT-N5100','JZO54K','GT-N7100','KOT49H','GT-N8000','JZO54K','GT-N8000','KOT49H','GT-P3110','JZO54K','GT-P5100','IML74K','GT-P5100','JDQ','GT-P5100','JDQ39','GT-P5100','JZO54K','GT-P5110','JDQ39','GT-P5200','KOT49H','GT-P5210','KOT49H','GT-P5220','JDQ39','GT-S7390','JZO54K','SAMSUNG','SM-A500F','SAMSUNG','SM-G532F','SAMSUNG','SM-G920F','SAMSUNG','SM-G935F','SAMSUNG','SM-J320F','SAMSUNG','SM-J510FN','SAMSUNG','SM-N920S','SAMSUNG','SM-T280','SM-A500FU','MMB29M','SM-A500F','LRX22G','SM-A500F','MMB29M','SM-A500H','MMB29M','SM-G900F','KOT49H','SM-G920F','MMB29K','SM-G920F','NRD90M','SM-G930F','NRD90M','SM-G935F','MMB29K','SM-G935F','NRD90M','SM-G950F','NRD90M','SM-J320FN','LMY47V','SM-J320F','LMY4','SM-J320F','LMY47V','SM-J320H','LMY47V','SM-J320M','LMY47V','SM-J510FN','MMB29M','SM-J510FN','NMF2','SM-J510FN','NMF26X','SM-J510FN','NMF26X;','SM-J701F','NRD90M;','SM-T111','JDQ39','SM-T230','KOT49H','SM-T231','KOT49H','SM-T235','KOT4''SM-T310','KOT49H','SM-T311','KOT4','SM-T311','KOT49H','SM-T315','JDQ39','SM-T525','KOT49H','SM-T531','KOT49H','SM-T531','LRX22G','SM-T535','LRX22G','SM-T555','LRX22G','SM-T561','KTU84P','SM-T705','LRX22G','SM-T705','LRX22G','SM-T805','LRX22G','SM*T820','NRD90M','SPH-L720','KOT49H'])
			gttt=random.choice(['GT-I9190','KOT49H','GT-I9192','KOT49H','GT-I9300I','KTU84P','GT-I9300','IMM76D','GT-I9300','JSS15J','GT-I9301I','KOT4','GT-I9301I','KOT49H','GT-I9500','JDQ39','GT-I9500','LRX22C','GT-N5100','JZO54K','GT-N7100','KOT49H','GT-N8000','JZO54K','GT-N8000','KOT49H','GT-P3110','JZO54K','GT-P5100','IML74K','GT-P5100','JDQ','GT-P5100','JDQ39','GT-P5100','JZO54K','GT-P5110','JDQ39','GT-P5200','KOT49H','GT-P5210','KOT49H','GT-P5220','JDQ39','GT-S7390','JZO54K','SAMSUNG','SM-A500F','SAMSUNG','SM-G532F','SAMSUNG','SM-G920F','SAMSUNG','SM-G935F','SAMSUNG','SM-J320F','SAMSUNG','SM-J510FN','SAMSUNG','SM-N920S','SAMSUNG','SM-T280','SM-A500FU','MMB29M','SM-A500F','LRX22G','SM-A500F','MMB29M','SM-A500H','MMB29M','SM-G900F','KOT49H','SM-G920F','MMB29K','SM-G920F','NRD90M','SM-G930F','NRD90M','SM-G935F','MMB29K','SM-G935F','NRD90M','SM-G950F','NRD90M','SM-J320FN','LMY47V','SM-J320F','LMY4','SM-J320F','LMY47V','SM-J320H','LMY47V','SM-J320M','LMY47V','SM-J510FN','MMB29M','SM-J510FN','NMF2','SM-J510FN','NMF26X','SM-J510FN','NMF26X;','SM-J701F','NRD90M;','SM-T111','JDQ39','SM-T230','KOT49H','SM-T231','KOT49H','SM-T235','KOT4''SM-T310','KOT49H','SM-T311','KOT4','SM-T311','KOT49H','SM-T315','JDQ39','SM-T525','KOT49H','SM-T531','KOT49H','SM-T531','LRX22G','SM-T535','LRX22G','SM-T555','LRX22G','SM-T561','KTU84P','SM-T705','LRX22G','SM-T705','LRX22G','SM-T805','LRX22G','SM*T820','NRD90M','SPH-L720','KOT49H'])
			android_version=str(random.randrange(6,13))
			ua_string = f'Davik/2.1.0 (Linux; U; Android {str(android_version)}.0.0; {str(gtt)} Build/{str(gttt)} [FBAN/FB4A;FBAV/{str(application_version)};FBBV/{str(application_version_code)};FBDM/'+'{density=1.5,width=480,height=800}'+f';FBLC/pl_PL;FBCR/T-Mobile.pl;FBMF/samsung;FBBD/samsung;FBPN/{str(fbs)};FBDV/{str(gtt)};FBSV/4.4.4;nullFBCA/armeabi-v7a:armeabi;]'
			adid = str(uuid.uuid4())
			data = {
				"adid": adid,
				"email": user,
				"password": pw,
				"cpl": "true",
				"credentials_type": "device_based_login_password",
				"source": "device_based_login",
				"error_detail_type": "button_with_disabled",
				"source": "login", "format": "json",
				"generate_session_cookies": "1",
				"generate_analytics_claim": "1",
				"generate_machine_id": "1",
				"locale": "pl_PL", "client_country_code": "PL",
				"device": gtt,
				"device_id": adid,
				"method": "auth.login",
				"fb_api_req_friendly_name": "authenticate",
				"fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler"
			}

			head = {
				"content-type": "application/x-www-form-urlencoded",
				"x-fb-sim-hni": str(random.randint(2e4,4e4)),
				"x-fb-connection-type": "unknown",
				"Authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32",
				"user-agent": ua_string,
				"x-fb-net-hni": str(random.randint(2e4,4e4)),
				"x-fb-connection-bandwidth": str(random.randint(2e7,3e7)),
				"x-fb-connection-quality": "EXCELLENT",
				"x-fb-friendly-name": "authenticate",
				"accept-encoding": "gzip, deflate",
				"x-fb-http-engine": "Liger"
			}
			rest = ses.post("https://b-api.facebook.com/method/auth.login", data=data, headers=head, allow_redirects=False).text
			result = json.loads(rest)
			return result