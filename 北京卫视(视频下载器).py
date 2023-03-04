import re
import tkinter as tk
import tkinter.messagebox
import requests
from tkinter.filedialog import askdirectory
import os


def down_load():
    try:
        url = video_url.get()
        url_ = tk.messagebox.showinfo('操作提示', '确定要下载该视频吗?')
        if url_:
            name = url.split('/')[-1]
            url = 'https://app.api.btime.com/video/play?id=' + name
            h = {
                'cookie': '__guid=ddf677be-b8a2-11ed-a059-6c92bf0ad279; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22186a02c84e34-0f75ebe9ce6a55-74525471-1327104-186a02c84e4a4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.msn.cn%2F%22%7D%2C%22%24device_id%22%3A%22186a02c84e34-0f75ebe9ce6a55-74525471-1327104-186a02c84e4a4%22%7D; __lid=; usid=41f1d567b063469e793d71da7ae97e7b; __DC_gid=196757375.14410235.1677724517741.1677725282094.5; z_api_request_time=0.0014519691467285',
                'referer': 'https://item.btime.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
            }
            text = requests.get(url='https://item.btime.com/' + name, headers=h).text
            title = re.findall('<title>(.*?)</title>', text, re.S)[0].strip()
            title = re.sub(r'[\\/:*?<>|]', '', title)
            r = requests.get(url=url, headers=h).json()
            url_V = r['data']['video_stream'][0]['stream_url']
            DATA = requests.get(url=url_V)
            DATA = DATA.content
            with open(f'{title}.mp4', 'wb') as f:
                f.write(DATA)
            tk.messagebox.showinfo('操作提示', '视频已保存至本地!')
    except:
        tk.messagebox.showerror('操作提示', '视频地址输入有误！')


def exit_():
    Cancel = tk.messagebox.askyesno('操作提示', '是否要退出程序?')
    if Cancel:
        root.quit()


def clear_entry():  # 取消录入
    video_url.set('')


def selectPath():
    try:
        path_ = askdirectory()  # 使用askdirectory()方法返回文件夹的路径
        if path_ == "":
            path.get()  # 当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
        else:
            path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
            path.set(path_)
        os.chdir(path_)
        print('默认下载地址已更换为', os.getcwd())
    except:
        pass


def openPath():
    try:
        dir = os.path.dirname(path.get() + "\\")
        os.system('start ' + dir)
    except:
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title('BRTV视频下载器')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 500
    height = 200
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2
    size = f'{width}x{height}+{int(x)}+{int(y)}'
    root.geometry(size)
    root.iconbitmap("BRTV.ico")
    root.attributes("-alpha", 0.9)
    font = ('华文行楷', 16)
    tk.Label(root, text='请输入视频地址:', font=font, height=3).grid(row=1, column=1)
    video_url = tk.StringVar()
    video_url.set('请将视频地址粘贴至此处')
    tk.Entry(root, textvariable=video_url, width=45).grid(row=1, column=2)
    path = tk.StringVar()
    path.set(os.path.abspath("."))
    tk.Label(root, font=font, text="目标路径:").grid(row=2, column=1)
    tk.Entry(root, textvariable=path, width=45, state="readonly").grid(row=2, column=2)
    tk.Label(root, text='仅限下载https://www.btime.com/btv的视频（@Klcok）').place(x=185, y=170)
    btnSubmit_entry = tk.Button(root, text='下载视频', command=down_load, relief="groove", bd=8).place(x=30, y=125)
    btnCancel_entry = tk.Button(root, text='退出程序', command=exit_, relief="groove", bd=8).place(x=130, y=125)
    path_select = tk.Button(root, text="路径选择", command=selectPath, relief="groove", bd=8).place(x=230, y=125)
    open_file = tk.Button(root, text="打开文件位置", command=openPath, relief="groove", bd=8).place(x=330, y=125)
    fresh = tk.Button(root, text='刷新', command=clear_entry, relief="raised", bd=6).place(x=450, y=125)
    root.mainloop()
