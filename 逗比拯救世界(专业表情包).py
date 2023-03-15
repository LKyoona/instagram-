import requests
import os

if not os.path.exists('逗比图库'):
    os.mkdir('逗比图库')
else:
    pass
times = input('请输入下载数量单位(百):')
for i in range(int(times)):
    url = 'https://www.dbbqb.com/api/search/json?size=100'
    headers = {
        'Cookie': 'F12开发者工具复制自己的cookies',
        'Host': 'www.dbbqb.com',
        'Referer': 'https://www.dbbqb.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61',
        'Web-Agent': 'web',
    }
    response = requests.get(url=url, headers=headers).json()
    for data in response:
        img_url = 'https://image.dbbqb.com/' + data['path']
        img_data_type = requests.get(url=img_url).headers
        img_type = '.' + img_data_type['Content-Type'].split('/')[-1]
        img_data = requests.get(url=img_url).content
        title = img_url.split('/')[-1]
        f = open('逗比图库\\' + title + img_type, 'wb')
        f.write(img_data)
        f.close()
        print('---' + title + img_type + '已写入逗比图库---')
