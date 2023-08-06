import requests
def InfoTik(user):
    res = requests.get(f'https://api.dlyar-dev.tk/info-tiktok.json?user={user}').json()
    if res['status'] == True:
        qq = res['id']
        ww = res['name']
        ee = res['country']
        rr = res['code-country']
        tt = res['flag']
        yy = res['followers']
        uu = res['following']
        ii = res['likes']
        oo = res['video']
        return {'result':'true','id':qq,'name':ww,'country':ee,'code-country':rr,'flag':tt,'followers':yy,'following':uu,'likes':ii,'video':oo,'By':'@X_6_Z'}
    else:
        return {'result':'false','By':'@X_6_Z'}