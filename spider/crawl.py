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
        'cookie': 'RK=gQholRlvNm; ptcz=0e6f9ebf593f91620325f6c08506b6a2a5f2bb56968575544b505725c4800946; pgv_pvid=7890639705; o_cookie=438396211; ied_qq=o0438396211; fqm_pvqid=b6675d70-2780-45b7-9f63-5e91e8dfac64; tvfe_boss_uuid=8199742223d704d9; pt_235db4a7=uid=7b092MkEjQ7eGHT8-YuoQg&nid=1&vid=4kFTcKmYfB/GPx0i097DIw&vn=1&pvn=1&sact=1650248612488&to_flag=0&pl=0KzaISwJA-wYoyVB1nkjpQ*pt*1650248612488; pac_uid=1_438396211; iip=0; uin_cookie=o0438396211; clickNums=1; eas_sid=Y1K637k2T2N9t1k7c3i103J3m0; LW_uid=r1n6H7z2W5O7f6t8r3o1q6I8m7; _t_qbtool_uid=aaaaun9bfl22sdxhzn5k1ufxizvt88cb; tmeLoginType=2; wxrefresh_token=; euin=7eoFoiEsow65; wxopenid=; psrf_qqopenid=6451A9D7A02F727C83A985460E5B6F5A; psrf_qqunionid=C32F90C41C4E34FA809B5776EF3428E9; wxunionid=; psrf_qqaccess_token=3BB4CC5F3D32F6397B8C63B4707715D0; psrf_qqrefresh_token=20A71EA151E59A897E745D667C01C176; psrf_access_token_expiresAt=1685974943; isHostDate=19427; PTTuserFirstTime=1678492800000; ts_refer=www.baidu.com/link; ts_uid=4153368797; weekloop=0-0-0-10; isOsSysDate=19427; PTTosSysFirstTime=1678492800000; isOsDate=19427; PTTosFirstTime=1678492800000; tgl_sid=cc921c4f2f777e767195f18dea0328ddb7c4425b; tglLoginType=qq; login_type=qqpc; ieg_ingame_userid=OYHhD2uLsBc4NugatfBA9uTMNrQPbFmM; pgv_info=ssid=s6870265232; _qpsvr_localtk=0.9820986972224304; LW_sid=n1Q6q7L8E574o5b2T5l6h8i7J0; eas_entry=https%3A%2F%2Fmilo.qq.com%2F; openid=4B743628F6E9CBEA7206DF5BDB2083B1; access_token=34EE1A0DF0BF4B2BBD3C536916E0EB03; appid=101491592; acctype=qc; pt2gguin=o0438396211; PVP_PERSONAL_DATA_null=areaid%3D1%26areaname%3D%25E6%2589%258BQ171%25E5%258C%25BA-%25E7%25BB%25BD%25E9%25A3%258E%25E5%258D%258E%26roleid%3D29E41E2A428952F2F1E41CAB5E378747%26rolename%3D%25E8%25B5%25B5%25E2%2599%259F%25E9%25A3%259E%253F%25E5%2582%25BB%26rolesex%3D%26rolejob%3D%26checkparam%3Dyxzj%257Cyes%257C29E41E2A428952F2F1E41CAB5E378747%257C1%257C29E41E2A428952F2F1E41CAB5E378747*%257C29E41E2A428952F2F1E41CAB5E378747%257C%257C1181%257C%2525E8%2525B5%2525B5%2525E2%252599%25259F%2525E9%2525A3%25259E%25253F%2525E5%252582%2525BB*%257C%257C%257C1678545413%257C1181%25255F29E41E2A428952F2F1E41CAB5E378747*%26md5str%3D6FE5A18242A5422D8C3C39CAF4161B6A%26roleareaid%3D1%26sPartition%3D1181; IED_LOG_INFO_NEW=acctype%3Dqc%26openid%3D4B743628F6E9CBEA7206DF5BDB2083B1%26nickName%3D13765986%26avatarUrl%3Dhttp%253A%252F%252Fthirdqq.qlogo.cn%252Fg%253Fb%253Doidb%2526k%253DicGRY72lxewVficMeTD2EE5g%2526kti%253DZAySBwAAAAE%2526s%253D40%2526t%253D1483445884; pvpqqcomrouteLine=index_personal_personal_personal_hisrecord_hisrecord_artdetail; ts_last=pvp.qq.com/web201605/herolist.shtml; PTTDate=1678546419151'}
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
