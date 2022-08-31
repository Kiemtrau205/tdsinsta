import requests, json
import _testimportmultiple
from requests.structures import CaseInsensitiveDict

import os, time, sys
config = json.load(open('config.json','r'))
token = config['token_tds']
like = config['type']['heart']['get_list']
cLike = config['type']['heart']['duyet_nv']
follow = config['type']['follow']['get_list']
cFollow = config['type']['follow']['duyet_nv']
with open('cookie.txt','r') as f:
  cookie = f.read()
  f.close()
def banner():
  os.system('cls' if os.name=='nt' else 'clear')
  logo = """
  -----------------------------------
  -- >        TDS Instagram      < --
  --       by Kiemmanowar          --
  -----------------------------------\n""" 
  for x in logo:
    sys.stdout.write(x)
    sys.stdout.flush()
    time.sleep(0.0001)

banner() 
def headers(csrf_token):
  headers = CaseInsensitiveDict()
  headers["authority"] = "www.instagram.com"
  headers["accept"] = "*/*"
  headers["sec-ch-prefers-color-scheme"] = "dark"
  headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
  headers["x-csrftoken"] = csrf_token
  headers["x-requested-with"] = "XMLHttpRequest"
  headers["x-instagram-ajax"] = "1005951515"
  headers["x-requested-with"] = "XMLHttpRequest"
  return headers


def getUserInfo(cookie):
  url = "https://www.instagram.com/data/shared_data/"
  rq = requests.get(url, cookies=cookie).json()
  json_data = rq['config']['viewer']
  return json_data['username']
def delay(times):
  x = 1
  for i in range(times, -1, -1):
    print(f"Wait for {i}s {'~'*x}", end='\r')
    x+=1
    time.sleep(1)
def action(id, cookie, type):
  if type == 1:
    urlAction = "https://www.instagram.com/web/friendships/" + id + "/follow/"
  elif type == 2:
    urlAction = "https://www.instagram.com/web/likes/" + id + "/like/"

  url = "https://www.instagram.com/data/shared_data/"
  rq = requests.get(url, cookies=cookie).json()
  csrf_token = rq['config']['csrf_token']
  resp = requests.post(urlAction, headers=headers(
        csrf_token), cookies=cookie)
  try:
    return resp.json()['status'] == 'ok'
  except:
    return False  
def cookie_to_dict(cookie):
  dic = {}
  cks = cookie.split(';')
  for x in cks:
    chk = x.split('=')
    if len(chk)==2:
      def lam(x): return x.replace(' ',"")
      dic[lam(chk[0])] = lam(chk[1])
  return dic
def tds(token, cookie):
  cookies = cookie_to_dict(cookie)
  
  url = "https://traodoisub.com/api/?fields=profile&access_token=" + token
  resp = requests.get(url).json()
  print(f"[+]Tài khoản : {resp['data']['user']} <> [+]Coins : {resp['data']['xu']}")
  print(f"=> Đăng nhập thành công {getUserInfo(cookies)}")
  x = 0
  while True:
    try:
      listJobsFl = requests.get(f'https://traodoisub.com/api/?fields={follow}&access_token={token}').json()
      listJobsL = requests.get(f'https://traodoisub.com/api/?fields={like}&access_token={token}').json()
      if len(listJobsFl['data'])!=0:
        id = listJobsFl['data'][0]['id']
        idSplit = id.split('_')[0]
        link = listJobsFl['data'][0]['link']
        followU = action(idSplit,cookies,1)
        if followU:
          
          sendR = requests.get(f"https://traodoisub.com/api/coin/?type={cFollow}&id={id}&access_token={token}").json()
          print(f"[{x}] FOLLOW | {link} | {sendR['data']['msg']} | {sendR['data']['pending']} | {sendR['data']['cache']} \n")
          x+=1
          delay(5)
        else:
          print('FAILED')
      if len(listJobsL['data'])!=0:
        id = listJobsL['data'][0]['id']
        idSplit = listJobsL['data'][0]['id'].split('_')[0]
        link = listJobsL['data'][0]['link']
        likeU = action(idSplit,cookies,2)
        if likeU:
          
          sendR = requests.get(f"https://traodoisub.com/api/coin/?type={cLike}&id={id}&access_token={token}").json()
          sr = sendR['data']
          print(f"[{x}] | LIKE | {link} | {sr['msg']} | {sr['pending']} | {sr['cache']} \n")
          x+=1
          delay(5)
        else:
          print('FAILED')
      else:
        print('=> [!] Đang Tìm Job .', end='\r')
        time.sleep(0.025)
        print('=> [/] Đang Tìm Job ..', end='\r')
        time.sleep(0.025)
        print('=> [-] Đang Tìm Job ...', end='\r')
        time.sleep(0.025)
        print('=> [\] Đang Tìm Job ....', end='\r')
        time.sleep(0.025)
    except Exception as e:
      print(e)
      continue
tds(token, cookie)