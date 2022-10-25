'''
Instargram爬取人名单
'''
# 设置保存艺人文件夹的名字
Username = 'TaeYeon'
# 设置需要爬取的用户名
USER_NAME = 'taeyeon_ss'
# 设置用户名的ID,ID在开发者工具里面搜索target_id参数即可找到用户名ID
USER_ID = "329452045"
# 设置截止页码
END_PAGE = 5
'''设置headers请求头获取第一页的数据,一旦发现与请求头的数据不一致请及时更换'''
X_CSRF_TOKEN = 'HtJi7wiHTQWRw9vNlBHaHPLTe1IXsOJQ'
x_ig_www_claim = 'hmac.AR3c2KhaEtGIIzPntsMALvl6NhqmI6DK1r9_b4Ev88oKIxJ0'
x_instagram_ajax = '1006449831'
# 如若cookies失效,请及时更换cookie
COOKIES = 'mid=YlFTTwALAAERy7VgxyADDyAuTKBb; ig_did=5016A6A1-AA23-44CB-A71B-883155F282AB; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; datr=i76gYqY1Dm_BZSlkbuz0iBUu; dpr=1.25; ds_user_id=31954829244; csrftoken=HtJi7wiHTQWRw9vNlBHaHPLTe1IXsOJQ; shbid="19616\05431954829244\0541698233009:01f7323d5c8e02abd7bfc1a216b9bb16860be74068e99fe897f0bb6df1c2d723797a1475"; shbts="1666697009\05431954829244\0541698233009:01f762b01b206047b3b4e0940ee4c5e0a491f0217a0db600f6810408c0ee099f91bf9173"; sessionid=31954829244%3AGZmYhMJQUpY96U%3A8%3AAYeimn7Nu2wjRYvH6AJ1VUVUw5D_wKi6e8JSveIU1A; rur="VLL\05431954829244\0541698244406:01f7dba08c5822312f6d6052ad0b24622c48a37db465d677b01a18fdddd21580432af8c1"'
