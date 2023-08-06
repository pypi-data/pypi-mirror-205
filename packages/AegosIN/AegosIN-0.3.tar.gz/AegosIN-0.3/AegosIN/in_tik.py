import requests
def InfoTik(user):
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