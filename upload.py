import requests
import os
import re
import json
import base64
import sys

url1 = 'https://member.bilibili.com/preupload?name={}&size={}&r=upos&profile=ugcupos%2Fbup&ssl=0&version=2.8.12&build=2081200&upcdn=qn&probe_version=20200810'
url2 = 'https://upos-sz-upcdnqn.bilivideo.com/ugcboss/{}?uploads&output=json'
url3 = 'https://upos-sz-upcdnqn.bilivideo.com/ugcboss/{}?partNumber={}&uploadId={}&chunk={}&chunks={}&size={}&start={}&end={}&total={}'
url4 = 'https://upos-sz-upcdnqn.bilivideo.com/ugcboss/{}?output=json&name={}&profile=ugcupos%2Fbup&uploadId={}&biz_id={}'
url5 = 'https://member.bilibili.com/x/vu/web/cover/up'
url6 = 'https://member.bilibili.com/x/vu/web/add?csrf={}'


class upload:
    header = {
        'cookie': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    }

    data = {
        'copyright': 1,
        'cover': '',
        'desc': '',
        'desc_format_id': 32,
        'dynamic': '',
        'interactive': 0,
        'mission_id': 16177,
        'no_reprint': 1,
        'subtitle': {
            'open': 0,
            'lan': ""
        },
        'tag': '',
        'tid': 0,
        'title': '',
        'up_close_danmu': False,
        'up_close_reply': False,
        'videos': [
            {
                'filename': '', 
                'title': '', 
                'desc': '', 
                'cid': ''
            }
        ]
    }
    
    def __init__(self,config = {}) -> None:
        self.config = config
        self.setconfig()
        
    def setconfig(self) -> None:
        try:
            self.header['cookie'] = self.config['cookie']
            if len(re.findall(r'bili_jct=(\S+?);',self.config['cookie'])):
                self.bili_jct = re.findall(r'bili_jct=(\S+?);',self.config['cookie'])[0]
            else:
                self.bili_jct = re.findall(r'bili_jct=(\S+?)$',self.config['cookie'])[0]
        except Exception:
            print('cookie error')
            sys.exit()

        try:
            self.video_path = self.config['video_path']
            self.cover_path = self.config['cover_path']
            self.data['desc'] = self.config['desc']
            self.data['tag'] = self.config['tag']
            self.data['tid'] = self.config['tid']
            self.data['title'] = self.config['title']
            if 'copyright' in self.config:
                self.data['copyright'] = self.config['copyright']
            if 'dynamic' in self.config:
                self.data['dynamic'] = self.config['dynamic']
            if 'no_reprint' in self.config:
                self.data['no_reprint'] = self.config['no_reprint']
            if 'subtitle' in self.config:
                self.data['subtitle'] = self.config['subtitle']
            if 'up_close_danmu' in self.config:
                self.data['up_close_danmu'] = self.config['up_close_danmu']
            if 'up_close_reply' in self.config:
                self.data['up_close_reply'] = self.config['up_close_reply']
        except Exception:
            print('config error')
            sys.exit()

    def picture_upload(self) -> None:
        try:
            with open(self.cover_path,'rb+') as file:
                print('正在上传封面')
                code = b'data:image/jpeg;base64,'+base64.b64encode(file.read())
                js = json.loads(requests.post(url5,data={'cover': code,'csrf': self.bili_jct},headers=self.header).text)
                self.data['cover'] = js['data']['url'].split(':')[1]
                print('封面上传完毕')
        except Exception:
            print('封面路径无效')
            sys.exit()

    def video_upload(self) -> None:
        try:
            print('正在上传视频')
            header = self.header
            video_path = self.video_path
            video_name = video_path.split('\\')[-1]
            size = os.path.getsize(video_path)
            js1 = json.loads(requests.get(url1.format(video_name,size),headers=header).text)
            header['X-Upos-Auth'] = js1['auth']
            upos_uri = js1['upos_uri'].split('/')[-1]
            biz_id = js1['biz_id']
            js2 = json.loads(requests.post(url2.format(upos_uri),headers=header).text)
            upload_id = js2['upload_id']

            with open(video_path,'rb+') as file:
                requests.put(url3.format(upos_uri,1,upload_id,0,1,size,0,size,size),headers=header,data=file.read())
            js3 = requests.post(url4.format(upos_uri,video_name,upload_id,biz_id),headers=header).text
            if 'OK' in js3:
                print('视频上传完毕')

            self.data['videos'][0]['filename'] = upos_uri.split('.')[0]
            self.data['videos'][0]['cid'] = biz_id
            self.data['videos'][0]['title'] = video_name.split('.')[0]
        except IOError:
            print('视频路径无效')
        except KeyError:
            print('视频配置出错')

    def upload(self) -> None:
        self.picture_upload()
        self.video_upload()

        js = json.loads(requests.post(url6.format(self.bili_jct),headers=self.header,data=json.dumps(self.data).encode('utf-8')).text)
        if js['code'] != 0:
            print(js['message'])
        else:
            print('投稿成功')
            print('av:{}, bv:{}'.format(js['data']['aid'],js['data']['bvid']))