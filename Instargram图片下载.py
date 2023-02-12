import re
import requests
import time
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
    print(requests.get(url=url, headers=headers, params=params, verify=False).status_code)
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
                title = re.findall('(.*)_n.*\?stp=', img_url.split('/')[5])[0]
                print(title)
                with open(title + '.jpg', 'wb') as f:
                    f.write(data)
            print(f'爬完了第1页!')
        except Exception as e:
            print(e)  # 遇到反爬
            save_img(Img_list)  # 反复调用 想阻止我爬图！ 你休想！

    save_img(Img_list)
    return end_cursor


# 第一页
def parse_pages(next_page, num=1):
    '''id参数在这个函数里面url里'''
    # 设置截止页码
    if num == END_PAGE:
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
        # 查询下一页参数
        next_page = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        num += 1
        # 获取到12个图片详情地址
        img_list = json_data['data']['user']['edge_owner_to_timeline_media']['edges']
        Img_list = []
        print(requests.get(url=url, headers=headers, verify=False).status_code)
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
                    with open(title + '.jpg', 'wb') as f:
                        f.write(data)
                print(f'爬完了第{num}页!')
            except Exception as e:
                # 遇到反爬
                print(e)
                # 反复调用 想阻止我爬图！ 你休想！
                save_img(Img_list)

        save_img(Img_list)
        # 实现自动翻页自己调用自己 出口也就是翻页的最后一页
    return parse_pages(next_page, num)


def main():
    end_cursor = ins_first(User_name)
    parse_pages(end_cursor)


if __name__ == '__main__':
    User_name = USER_NAME
    start = time.time()
    main()
    print('爬完了！')
    print('花费了时间:%d秒' % (time.time() - start))
