import os
import re
import time
import json
import parsel
import requests
import concurrent.futures

if not os.path.exists('img'):
    os.mkdir('img')
with open('ALL_DATA.json', 'r', encoding='utf-8') as f:
    ALL_DATA = json.loads(f.read())


def send_requests(url):
    bit = requests.get(url=url).content
    return bit


def save(hero, skin, bit):
    with open('img\\' + hero + '-' + skin + '.jpg', 'ab') as f:
        f.write(bit)
    print(hero + '-' + skin)


def main(hero, skin, url):
    bit = send_requests(url=url)
    save(hero, skin, bit)


if __name__ == '__main__':
    T1 = time.time()
    url = 'https://pvp.qq.com/web201605/js/herolist.json'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'}
    cookie = {
        'cookie': '请自行更换自己的cookie'}
    json_data = requests.get(url=url, headers=headers).json()
    f = open('json_data.json', 'w', encoding='utf-8')
    f.write(json_data)
    f.close()
    HERO_LIST = []
    HERO_DICT = []
    for data in json_data:
        p_id = data['ename']
        hero_name = data['cname']
        HERO_LIST.append((p_id, hero_name))
    for id, name in HERO_LIST:
        hero_url = f'https://pvp.qq.com/web201605/herodetail/{id}.shtml'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'}
        html = requests.get(url=hero_url, headers=headers)
        html.encoding = 'gbk'
        selector = parsel.Selector(html.text)
        skins = selector.css('ul.pic-pf-list::attr(data-imgname)').get()
        skins = re.sub('&\d+', '', skins)
        HERO_DICT.append({'id': id, 'hero_name': name, 'skins': skins})
    ALL_DATA = []
    for hero_data in HERO_DICT:
        # 英雄名称
        hero_name = hero_data['hero_name']
        # 英雄id
        id = hero_data['id']
        skins = hero_data['skins'].split('|')
        for i in range(1, len(skins) + 1):
            # 皮肤名称
            skin_name = skins[i - 1]
            skin_url = f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{id}/{id}-mobileskin-{i}.jpg'
            ALL_DATA.append({'英雄名': hero_name, '皮肤名': skin_name, 'url': skin_url})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for data in ALL_DATA:
            hero = data['英雄名']
            skin = data['皮肤名']
            url = data['url']
            executor.submit(main, hero, skin, url)
    print('花费了' + str(round(time.time() - T1, 2)) + '秒')
