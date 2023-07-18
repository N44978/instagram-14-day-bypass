import requests
import base64
from hashlib import sha1, md5
import os
import uuid
import requests
import string
import random
from time import time, sleep
from threading import Thread


class build_auth(object):
    def generate_username(self): 
        username = ( ''.join(random.choice(string.ascii_letters + string.digits) for i in range(5)) ) + "groo3"
        return username
    def returnCSRF(self): return sha1(os.urandom(64)).hexdigest()
    def returnUUID(self): return str(uuid.uuid4)
    def returnDeviceID(self): return "android-" + md5(self.returnUUID().encode("utf-8")).hexdigest()[:16]

    def __init__(self, username: str, password: str) -> None:
        self.HTTP_SESSION = requests.session()
        self.HTTP_SESSION.headers["User-Agent"] = "Instagram 5.9.2 Android (29/10; 420dpi; 1080x1794; Google/google; Android SDK built for x86_64; generic_x86_64; ranchu; db 'en_US; 132081655)" 
        # Change if gets patched. Grab from mobile.

        self.LOGIN_DATA     = '{}:{}'.format(username, password)

        self.SESSION_ID     = None
        self.IG_BEARER      = None
        self.FBID           = None

        self.RETURN_HEADERS = {}
        self.RETURN_DATA    = None
        self.Instagram_LOGIN()


    def Instagram_LOGIN(self):
        try:
        
            headers = {'Accept':'/','Accept-Encoding': 'gzip, deflate','Accept-Language': 'en-US','X-IG-Capabilities': '3brTvw==','X-IG-Connection-Type': 'WIFI','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','User-Agent': 'Instagram 135.0.0.17.129 Android (25/7.1.2; 320dpi; 900x1600; samsung; SM-G977N; beyond1q; qcom; en_US; 161478664)'}  

            data = {
                    'uuid': self.returnUUID(),
                    'username': self.LOGIN_DATA.split(':')[0],
                    'password': self.LOGIN_DATA.split(':')[1],
                    'device_id': self.returnDeviceID(),
                    'from_reg': 'false',
                    '_csrftoken': self.returnCSRF(),
                    'login_attempt_countn':'0',
                }

            login_data = self.HTTP_SESSION.post('https://i.instagram.com/api/v1/accounts/login/', headers=headers, data=data)

            if 'logged_in' in login_data.text:
                self.SESSION_ID = str(login_data.cookies).split('sessionid')[1].split('=')[1].split(' for')[0]
                print('signed in, trying to fetch FBID, IGUID, and Generating Bearer.')

                if self.IGBearerENCODING(): self.build_data()
            
            elif 'invalid' in login_data.text:
                print('Password or Username/Email was invalid')
                os._exit(0)
        except: print(login_data.text)


    def FETCH_UID(self):
        raw = self.HTTP_SESSION.get('https://i.instagram.com/api/v1/users/web_profile_info/?username=' + self.LOGIN_DATA.split(':')[0], headers={'User-Agent':'Instagram 255.0.0 Android; 456141817'}).text
        try:
            fb_id, ig_uid  = raw.split('"fbid":"')[1].split('","')[0], raw.split('"id":"')[1].split('","is_business')[0]
            print('\n{} is the Current username on the account | UID: {}'.format(raw.split('"username":"')[1].split('","')[0], ig_uid))
            return fb_id, ig_uid
        except: 
            print(raw)
            print('Failed. Please restart')
        return

    def IGBearerENCODING(self):
        self.FBID, ds_user_id = self.FETCH_UID() 
        try:
            data_to_encode = '{"ds_user_id":"' + ds_user_id + '","sessionid":"' + self.SESSION_ID + '"}'
            self.IG_BEARER = str(base64.b64encode(bytes(data_to_encode, encoding='UTF-8'))).split("b'")[1].split("'")[0]
            return self.IG_BEARER
        except:
            print(data_to_encode)
            print('Failed. Restart.')

    def build_data(self):
        self.RETURN_HEADERS = {
            'Authorization': 'Bearer IGT:2:' + str(self.IG_BEARER),
            'User-Agent': 'Instagram 255.0.0 Android; 456141817',
            'X-Bloks-Version-Id': '4ed53fb65180cd94f1ba2b9ea62be383479d3bb84451fad4070bfec2b65785a2',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }  

        self.RETURN_DATA = 'params={"client_input_params":{"username":"%s","family_device_id":"6617589f-ec0b-4730-b34d-36382a080ea9"},"server_params":{"operation_type":"MUTATE","identity_ids":"%s"}}&bloks_versioning_id=4ed53fb65180cd94f1ba2b9ea62be383479d3bb84451fad4070bfec2b65785a2' %(self.generate_username(),self.FBID)
        print('Built DATA, Proceeding...')
        return  
    
    def check(self):
        rawjs = self.HTTP_SESSION.get('https://b.i.instagram.com/api/v1/accounts/current_user/?edit=true', headers={'user-agent':'Instagram 255.0.0 Android; 456141817)'}).json()   
        return rawjs['user']['trusted_username']


class INSTA_BYPASS_14DAY(object):
    def __init__(self, username:str, password:str):
        self.ACCOUNT_LOG = build_auth(username, password)
        self.RELEASE_DATA = self.ACCOUNT_LOG.RETURN_DATA
        self.HEADERS       = self.ACCOUNT_LOG.RETURN_HEADERS
        self.CLAIM_DATA  = 'params={"client_input_params":{"username":"%s","family_device_id":"6617589f-ec0b-4730-b34d-36382a080ea9"},"server_params":{"operation_type":"MUTATE","identity_ids":"%s"}}&bloks_versioning_id=4ed53fb65180cd94f1ba2b9ea62be383479d3bb84451fad4070bfec2b65785a2' %(username,self.ACCOUNT_LOG.FBID)
        self.SWAP_DELAYS = [0.518, 0.498,0.458,0.438,0.418,0.398]
        self.APPLY_LOG2 = float
        
        self.current_trusted = self.ACCOUNT_LOG.check()
        print('Current 14 DAY USER: ' + self.current_trusted)

        input('Press enter to bypass')  

        self.autoswap()
        self.ACCOUNT_LOG = build_auth(username, password)
        if self.ACCOUNT_LOG.check() != self.current_trusted:
            print('Successfully Bypassed 14 DAY')
            print('Saved username @', self.APPLY_LOG2)
        else: print('Failed')


    def APPLY_ORIGINAL(self, DELAY):
        sleep(DELAY)
        if 'account_identifiers' in requests.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.fxim.settings.username.change.async/',headers=self.HEADERS,data=self.CLAIM_DATA):
            print('bypassing...')

    def APPLY_BYPASS(self, DELAY):
        sleep(DELAY)
        raw = requests.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.fxim.settings.username.change.async/',headers=self.HEADERS,data=self.RELEASE_DATA)
        
        if 'account_identifiers' in raw.text:
            self.APPLY_LOG2 = time()
            self.APPLY_ORIGINAL(0)
        else:
            print('Failed')

    def autoswap(self):
        tmpThreads = []

        for DELAY in self.SWAP_DELAYS: tmpThreads.append(Thread(target=self.APPLY_ORIGINAL, args=(DELAY,)))
        for thread in tmpThreads: thread.start()

        Thread(target=self.APPLY_BYPASS,args=(0,)).start()
        return
    
    

INSTA_BYPASS_14DAY(input('username: '),input('password: '))
