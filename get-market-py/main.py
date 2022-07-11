import requests
import lzma
import io
import os
from json import dumps as jdumps
from decrypt_e import decrypt_e
from market_struct import dumpMarket

def getMarketPlainData():
    # 第一步：登录，获取 access_token
    loginUrl = 'http://datasrv.x07.top:8043/rpc/Login/LoginInterf/loginByUsername'

    headers = {'client-id': '1'}
    resp = requests.post(loginUrl, json={'username': 'test', 'password': 'testtest'}, headers=headers)
    # {'code': 0, 'timestamp': 1657378292030, 'message': 'Success',
    # 'data': {
    #    'oauth': {'access_token': 'xx', 'token_type': 'token', 'expires_in': 6841378292},
    #    'user': {'userid': 1, 'username': 'xx', 'email': 'xxx',
    #        'is_active': True, 'date_joined': 1456694700000, 'nickname': '', 'is_staff': True, 'vip_time': 1574352000000}},
    # 'status_code': 200}
    jobj = resp.json()
    if resp.status_code != 200:
        resp.raise_for_status()
    access_token = jobj['data']['oauth']['access_token']
    headers['access-token'] = access_token

    # 第二步：获取 market 文件（加密过的）
    marketUrl = 'http://stk-meta.x07.top/info-metas/MarketInfo.bin.e.xz'
    resp = requests.get(marketUrl)
    if resp.status_code != 200:
        resp.raise_for_status()
    with open('MarketInfo.bin.e.xz', 'wb') as fp:
        fp.write(resp.content)
    marketBytes = io.BytesIO(resp.content)
    data = lzma.open(marketBytes).read()
    print(len(data))
    with open('MarketInfo.bin.e', 'wb') as fp:
        fp.write(data)

    # 第三步：通过 market 文件信息获取解密秘钥
    chipherUrl = 'http://datasrv.x07.top:8043/rpc/KlineP2/KlineP2I/getFileCipher'
    resp = requests.post(chipherUrl, json={'cipherIn': {'fileName': 'MarketInfo.bin.e', 'fileSize': len(data)}}, headers=headers)

    if resp.status_code != 200:
        resp.raise_for_status()

    cipherOut = resp.json()['data']['cipherOut']

    # 第四步：解密
    plainData = decrypt_e(data, cipherOut['fileCipher'], access_token)
    with open('MarketInfo.bin', 'wb') as fp:
        fp.write(plainData)

if not os.path.exists('MarketInfo.bin'):
    getMarketPlainData()

with open('MarketInfo.bin', 'rb') as fp:
    dumpMarket(fp.read())
