import re
import threading
from pprint import pprint

import requests
import time
import concurrent.futures
import os
from config import Username, USER_NAME, USER_ID, COOKIES, END_PAGE
from config import X_CSRF_TOKEN, x_ig_www_claim, x_instagram_ajax

requests.packages.urllib3.disable_warnings()
try:
    os.mkdir(Username)
except:
    pass
finally:
    os.chdir(Username)


def ins_first(User_name):
    '''第一页'''
    url = 'https://i.instagram.com/api/v1/users/web_profile_info/'
    params = {'username': User_name}  # 传入从开发者工具获取到的用户名
    headers = {
        'cookie': COOKIES,
        'referer': f'https://www.instagram.com/{User_name}/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-asbd-id': '198387',
        'x-csrftoken': X_CSRF_TOKEN,
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': x_ig_www_claim,
        'x-instagram-ajax': x_instagram_ajax,
    }
    json_data = requests.get(url=url, headers=headers, params=params).json()
    end_cursor = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    img_list = json_data['data']['user']['edge_owner_to_timeline_media']['edges']  # 获取到12个图片详情地址
    Img_list = []
    Video_List = []
    for video_data in img_list:
        if video_data['node'].get('video_url') != None:
            Video_List.append(video_data['node']['video_url'])
        else:
            pass
    print(requests.get(url=url, headers=headers, params=params, verify=False).status_code)
    for img_data in img_list:
        if 'edge_sidecar_to_children' in img_data['node'].keys():
            for img in img_data['node']['edge_sidecar_to_children']['edges']:
                Img_list.append(img['node']['display_url'])
        else:
            Img_list.append(img_data['node']['display_url'])

    def save_img(Video_List):
        try:
            if len(Video_List) > 0:
                for video_url in Video_List:
                    data = requests.get(url=video_url, headers=headers, verify=False).content
                    title = re.findall('(.*)_n.mp4\?', video_url.split('/')[5])[0]
                    print(title)
                    Lock.acquire()
                    with open(title + '.mp4', 'wb') as f:
                        f.write(data)
                    Lock.release()
            for img_url in Img_list:
                data = requests.get(url=img_url, headers=headers, verify=False).content
                title = re.findall('(.*)_n.*?\?stp=', img_url.split('/')[5])[0]
                print(title)
                Lock.acquire()
                with open(title + '.jpg', 'wb') as f:
                    f.write(data)
                Lock.release()
            print(f'爬完了第1页!')
        except Exception as e:
            print(e)  # 遇到反爬
            save_img(Video_List)  # 反复调用 想阻止我爬图！ 你休想！

    print(save_img(Video_List))
    return end_cursor


Lock = threading.Lock()


# 第一页
def parse_pages(next_page, num=1):
    '''id参数在这个函数里面url里'''
    if num == END_PAGE:  # 设置截止页码
        return num
    else:
        headers = {
            'cookie': COOKIES,
            'referer': f'https://www.instagram.com/{User_name}/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        url = 'https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables={"id":"%s","first":12,"after":"%s"}' % (
            USER_ID, next_page)
        json_data = requests.get(url=url, headers=headers, verify=False).json()
        next_page = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']  # 查询下一页参数
        num += 1
        img_list = json_data['data']['user']['edge_owner_to_timeline_media']['edges']  # 获取到12个图片详情地址
        print(requests.get(url=url, headers=headers, verify=False).status_code)
        Img_list = []
        Video_List = []
        for video_data in img_list:
            if video_data['node'].get('video_url') != None:
                Video_List.append(video_data['node']['video_url'])
            else:
                pass
        for img_data in img_list:
            if 'edge_sidecar_to_children' in img_data['node'].keys():
                for img in img_data['node']['edge_sidecar_to_children']['edges']:
                    Img_list.append(img['node']['display_url'])
            else:
                Img_list.append(img_data['node']['display_url'])

        def save_img(Img_list, Video_List):
            try:
                if len(Video_List) > 0:
                    for video_url in Video_List:
                        data = requests.get(url=video_url, headers=headers, verify=False).content
                        title = re.findall('(.*)_n.mp4\?', video_url.split('/')[5])[0]
                        print(title)
                        Lock.acquire()
                        with open(title + '.mp4', 'wb') as f:
                            f.write(data)
                        Lock.release()
                for img_url in Img_list:
                    data = requests.get(url=img_url, headers=headers, verify=False).content
                    title = re.findall('(.*)_n.*?\?stp=', img_url.split('/')[5])[0]
                    print(title)
                    Lock.acquire()
                    with open(title + '.jpg', 'wb') as f:
                        f.write(data)
                    Lock.release()
                print(f'爬完了第{num}页!')
            except Exception as e:
                print(e)  # 遇到反爬
                save_img(Img_list, Video_List)  # 反复调用 想阻止我爬图！ 你休想！

        save_img(Img_list, Video_List)
    return parse_pages(next_page, num)  # 实现自动翻页自己调用自己 出口也就是翻页的最后一页


def main():
    '''第一个函数用于查参数'''
    global User_name
    User_name = USER_NAME
    end_cursor = ins_first(User_name)
    # 出口
    parse_pages(end_cursor)


if __name__ == '__main__':
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.submit(main)
    print('爬完了！')
    print('花费了时间:%d秒' % (time.time() - start))
