import re
import threading
import requests
import time
import concurrent.futures
import os

try:
    os.mkdir('Instagram图库')
except:
    pass
finally:
    os.chdir('Instagram图库')
requests.packages.urllib3.disable_warnings()


def ins_first(User_name):
    '''第一页'''
    url = 'https://i.instagram.com/api/v1/users/web_profile_info/'
    params = {'username': User_name}  # 传入从开发者工具获取到的用户名
    headers = {
        'cookie': 'dpr=1.5; ig_nrcb=1; ig_did=26A3D645-DFA8-4186-B203-47D1F16D3D6E; mid=Yz8y-AALAAGZXZ7NXwo50PgMsJfA; csrftoken=BVTJFPjMAaTt1RvFkxz1Qf0n3x3x7ms5; sessionid=31954829244%3ATuF3O9K928424A%3A16%3AAYeR99TMrQz-Slq1gh0xPzIL-Wlcmmk3ZUIEY4E59Q; ds_user_id=31954829244; shbid="19616\05431954829244\0541697193336:01f71ceba4147584164fd75826e0a4590f5c8cd3ffd285c6b9984dc6264f7a656c585d07"; shbts="1665657336\05431954829244\0541697193336:01f7bffdcac1be8139bcfefe924a711d808ed125ce974ad37fd3822a4d277e75a68ef31b"; datr=9-lHY_LI1SuAoswmC6G2VwBd; rur="NAO\05431954829244\0541697193449:01f7a012e5d65ca8ceccfdf3cd4ab355af9ca4442c5c05a3c56393353ce6edaee435ad21"',
        'referer': f'https://www.instagram.com/{User_name}/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-asbd-id': '198387',
        'x-csrftoken': 't8qOpdwo4X2V8yrxdnAlD9RLlHDRCGfG',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR3c2KhaEtGIIzPntsMALvl6NhqmI6DK1r9_b4Ev88oKI54K',
        'x-instagram-ajax': '1006382194'
    }
    json_data = requests.get(url=url, headers=headers, params=params).json()
    end_cursor = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    img_list = json_data['data']['user']['edge_owner_to_timeline_media']['edges']  # 获取到12个图片详情地址
    Img_list = []
    print(requests.get(url=url, headers=headers, verify=False).url)
    for img_data in img_list:
        if 'edge_sidecar_to_children' in img_data['node'].keys():
            for img in img_data['node']['edge_sidecar_to_children']['edges']:
                Img_list.append(img['node']['display_url'])
        else:
            Img_list.append(img_data['node']['display_url'])

    def save_img(Img_list):
        try:
            for img_url in Img_list:
                data = requests.get(url=img_url, headers=headers, verify=False).content
                title = re.findall('(.*)_n.jpg\?', img_url.split('/')[5])[0]
                Lock.acquire()
                with open(title + '.jpg', 'wb') as f:
                    f.write(data)
                Lock.release()
            print(f'爬完了第1页!')
        except Exception as e:
            print(e)  # 遇到反爬
            save_img(Img_list)  # 反复调用 想阻止我爬图！ 你休想！

    save_img(Img_list)
    return end_cursor

Lock = threading.Lock()


# 第一页
def parse_pages(next_page, num=1):
    '''id参数在这个函数里面url里'''
    if num == 3:  # 设置截止页码
        return num
    else:
        headers = {
            'cookie': 'dpr=1.5; ig_nrcb=1; ig_did=26A3D645-DFA8-4186-B203-47D1F16D3D6E; mid=Yz8y-AALAAGZXZ7NXwo50PgMsJfA; csrftoken=BVTJFPjMAaTt1RvFkxz1Qf0n3x3x7ms5; sessionid=31954829244%3ATuF3O9K928424A%3A16%3AAYeR99TMrQz-Slq1gh0xPzIL-Wlcmmk3ZUIEY4E59Q; ds_user_id=31954829244; shbid="19616\05431954829244\0541697193336:01f71ceba4147584164fd75826e0a4590f5c8cd3ffd285c6b9984dc6264f7a656c585d07"; shbts="1665657336\05431954829244\0541697193336:01f7bffdcac1be8139bcfefe924a711d808ed125ce974ad37fd3822a4d277e75a68ef31b"; datr=9-lHY_LI1SuAoswmC6G2VwBd; rur="NAO\05431954829244\0541697193449:01f7a012e5d65ca8ceccfdf3cd4ab355af9ca4442c5c05a3c56393353ce6edaee435ad21"',
            'referer': f'https://www.instagram.com/{User_name}/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        url = 'https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables={"id":"357021633","first":12,"after":"%s"}' % next_page
        json_data = requests.get(url=url, headers=headers, verify=False).json()
        next_page = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']  # 查询下一页参数
        num += 1
        img_list = json_data['data']['user']['edge_owner_to_timeline_media']['edges']  # 获取到12个图片详情地址
        Img_list = []
        print(requests.get(url=url, headers=headers, verify=False).url)
        for img_data in img_list:
            if 'edge_sidecar_to_children' in img_data['node'].keys():
                for img in img_data['node']['edge_sidecar_to_children']['edges']:
                    Img_list.append(img['node']['display_url'])
            else:
                Img_list.append(img_data['node']['display_url'])

        def save_img(Img_list):
            try:
                for img_url in Img_list:
                    data = requests.get(url=img_url, headers=headers, verify=False).content
                    title = re.findall('(.*)_n.jpg\?', img_url.split('/')[5])[0]
                    Lock.acquire()
                    with open(title + '.jpg', 'wb') as f:
                        f.write(data)
                    Lock.release()
                print(f'爬完了第{num}页!')
            except Exception as e:
                print(e)  # 遇到反爬
                save_img(Img_list)  #嗯？  想阻止我爬图片！ 你休想！

        save_img(Img_list)
    return parse_pages(next_page, num)  # 实现自动翻页自己调用自己 出口也就是翻页的最后一页


def main():
    '''第一个函数用于查参数'''
    global User_name
    # id 也要换
    User_name = input('请输入你要爬取的用户名:')
    end_cursor = ins_first(User_name)
    parse_pages(end_cursor)  # 出口


if __name__ == '__main__':
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.submit(main)
    print('爬完了！')
    print('花费了时间:%d秒' % (time.time() - start))
