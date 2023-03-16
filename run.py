import json
import os
import random
import threading
import time
from math import *
from tkinter import messagebox
from tkinter import *
import win32api
import webbrowser
import winsound
from PIL import Image, ImageTk
import pygame





def bind_1(event):  # 点击响应函数
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:  # 响应的位置
        global rectangle, tip_Text, font
        click_voice()
        '''-----------------------函数分割线-----------------------'''

        def skin_roll(i, number):
            global photo, counter, tip_Text, is_run, flag, skin_name, hero_flag

            show_member = random.choice(data)
            pre_image_file_path = 'assets/skin/' + show_member
            image = Image.open(pre_image_file_path)
            image = image.resize((500 // 2, 750 // 2))
            photo = ImageTk.PhotoImage(image)
            # 添加图像到标签
            skin_label = Label(win, image=photo)
            skin_label.place(x=275, y=115)
            wait = [a for a in range(100, 300, 10)] + [b for b in range(300, 600, 300 // (number - 28))] + \
                   [c for c in range(600, 1200, 120)]
            if i < number:
                win.after(wait[i], skin_roll, i + 1, number)
            else:
                SKIN_NAME = show_member.split('.png')[0]
                font = ('楷体', 22, 'bold')
                color = 'red'
                if len(SKIN_NAME) == 3 or 4 or 5 or 10 or 11:
                    tip_text_x, tip_text_y = 400, 515
                    tip_Text = canvas_.create_text(tip_text_x, tip_text_y, text=SKIN_NAME, font=font, fill=color)
                elif len(SKIN_NAME) == 6 or 7 or 8 or 9:
                    tip_text_x, tip_text_y = 403, 515
                    tip_Text = canvas_.create_text(tip_text_x, tip_text_y, text=SKIN_NAME, font=font, fill=color)
                winsound.PlaySound('assets/sound/close.wav', winsound.SND_ASYNC)

                def info():
                    win32api.MessageBox(None, '恭喜！ 您开出了{}'.format(SKIN_NAME.replace('-', '的')), '消息提示')

                time.sleep(0.1)
                threading.Thread(target=info).start()
                canvas_.itemconfigure(box_Text, text='开 箱')  # 重设显示文本内容
                is_run = False
                flag = True
                hero_flag = True
                skin_name = SKIN_NAME.split('-')[0]
                counter = 0

        def roll_start():
            global is_run, counter, tip_Text, flag, skin_name
            skin_name = ''
            is_run = True
            flag = False
            print(counter)
            if is_run and (counter == 0):
                # 添加Logo图像到标签
                Logo_label = Label(win, image=Logo_label_photo)
                Logo_label.place(x=275, y=-20)
                canvas_.itemconfigure(tip_Text, text="")
                canvas_.itemconfigure(box_Text, text='开 箱 中')  # 重设显示文本内容
                counter += 1
                number = int(random.uniform(21, 22))
                skin_roll(0, number)
                winsound.PlaySound('assets/sound/open.wav', winsound.SND_ASYNC)

            else:
                counter += 1
                print('进不来')

        def change_window():
            global hero_flag
            # 移除子窗口
            win.destroy()
            win.quit()
            # 重新显示主窗口
            root.iconify()
            root.deiconify()
            hero_flag = False

        def win_bind_1(event):
            global counter, change
            if 749 <= event.x <= 801 and 280 <= event.y <= 380:  # 响应的位置
                if flag:
                    counter = 0
                    change_window()
                    winsound.PlaySound('assets/sound/change.wav', winsound.SND_ASYNC)
            elif 340 <= event.x <= 475 and 540 <= event.y <= 585:  # 响应的位置
                roll_start()
            elif 5 <= event.x <= 57 and 260 <= event.y <= 400:  # 响应的位置
                if hero_flag:
                    with open('spider/json_data.json', 'r', encoding='utf-8') as f:
                        json_data = json.loads(f.read())
                        for data in json_data:
                            if skin_name == data['cname']:
                                id = data['ename']
                                hero_url = f'https://pvp.qq.com/web201605/herodetail/{id}.shtml'
                                webbrowser.open(hero_url, new=0)

        def win_bind_2(event):  # 鼠标经过响应函数
            if 749 <= event.x <= 801 and 280 <= event.y <= 380:  # 响应的位置
                canvas_.itemconfigure(return_rectangle, fill='black')  # 重设外框颜色
                canvas_.itemconfigure(return_oval1, fill='black')  # 重设内框颜色
                canvas_.itemconfigure(return_oval2, fill='black')  # 重设显示文本颜色
                canvas_.itemconfigure(return_text, fill='white')  # 重设显示文本颜色
                canvas_.configure(cursor='hand2')  # 重设鼠标样式
            elif 335 <= event.x <= 470 and 540 <= event.y <= 585:  # 响应的位置
                canvas_.itemconfigure(box_out_frame, outline='white')  # 重设外框颜色
                canvas_.itemconfigure(box_liner_frame, outline='white')  # 重设内框颜色
                canvas_.itemconfigure(box_Text, fill='white')  # 重设显示文本颜色
                canvas_.configure(cursor='hand2')  # 重设鼠标样式
            elif 5 <= event.x <= 57 and 260 <= event.y <= 400:  # 响应的位置
                canvas_.itemconfigure(select_hero_rectangle, fill='yellow')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_oval1, fill='yellow')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_oval2, fill='yellow')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_text, fill='#BF6C22')  # 重设显示文本颜色
                canvas_.configure(cursor='hand2')  # 重设鼠标样式
            else:
                canvas_.itemconfigure(return_rectangle, fill='')  # 重设显示文本颜色
                canvas_.itemconfigure(return_oval1, fill='')  # 重设显示文本颜色
                canvas_.itemconfigure(return_oval2, fill='')  # 重设显示文本颜色
                canvas_.itemconfigure(return_text, fill='black')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_rectangle, fill='')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_oval1, fill='')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_oval2, fill='')  # 重设显示文本颜色
                canvas_.itemconfigure(select_hero_text, fill='red')  # 重设显示文本颜色
                canvas_.itemconfigure(box_out_frame, outline='black')  # 重设外框颜色
                canvas_.itemconfigure(box_liner_frame, outline='black')  # 重设内框颜色
                canvas_.itemconfigure(box_Text, fill='black')  # 重设显示文本颜色
                canvas_.configure(cursor='arrow')  # 恢复鼠标样式

        '''-----------------------函数分割线-----------------------'''
        '-----------------------------------------------------------------------------------------'
        root.withdraw()
        win = Toplevel(root)
        win.title(' 欢迎来到王 者 荣 耀  ---皮 肤 抽 奖 池---')
        win.iconbitmap("assets/img/logo.ico")
        width = 800
        height = 600
        size = Gui(width, height)
        win.geometry(size)
        win.resizable(width=False, height=False)
        # -------------------------分割线-----------------------#
        bg = PhotoImage(file="assets/img/rand.png")
        canvas_ = Canvas(win, width=width, height=height, bd=0)
        canvas_.create_image(width // 2, height // 2, anchor='center', image=bg)
        canvas_.place(width=800, height=600)  # 设置Canvas控件大小及位置
        # -------------------------分割线-----------------------#
        tip_text_x, tip_text_y = 350, 515
        tip_Text = canvas_.create_text(tip_text_x, tip_text_y, text='')
        # Logo
        pre_image_file_path = 'assets/img/logo.png'
        image = Image.open(pre_image_file_path)
        image = image.resize((250, 185))
        Logo_label_photo = ImageTk.PhotoImage(image)

        def alive():
            pass

        win.protocol('WM_DELETE_WINDOW', alive)
        return_rectangle = canvas_.create_rectangle(750 - 1, 280, 800 + 1, 380, width=0, )  # 按钮外框
        return_oval1 = canvas_.create_oval(750, 250, 800, 300, width=0, )  # 按钮左圆
        return_oval2 = canvas_.create_oval(750, 350, 800, 400, width=0, )  # 按钮右圆
        return_text = canvas_.create_text(768, 340, text=' 点\n 我\n 返\n 回\n', font=('楷体', 20, 'bold'),
                                          fill='black')  # 按钮显示文本
        select_hero_rectangle = canvas_.create_rectangle(6 - 1, 260, 56 + 1, 400, width=0, )  # 按钮外框
        select_hero_oval1 = canvas_.create_oval(6, 230, 56, 320, width=0, )  # 按钮左圆
        select_hero_oval2 = canvas_.create_oval(6, 340, 56, 430, width=0, )  # 按钮右圆
        select_hero_text = canvas_.create_text(25, 340, text=' 查\n 看\n 英\n 雄\n 属\n 性\n', font=('楷体', 20, 'bold'),
                                               fill='red')  # 按钮显示文本
        box_out_frame = canvas_.create_rectangle(335, 540, 470, 585, width=4, outline='black')  # 按钮外框
        box_liner_frame = canvas_.create_rectangle(335 + 5, 540 + 5, 470 - 5, 585 - 5, width=3,
                                                   outline='black')  # 按钮内框
        box_text_x, box_text_y = round((335 + 470) / 2), round((540 + 585) / 2)
        box_Text = canvas_.create_text(box_text_x, box_text_y, text='开 箱', font=('楷体', 22, 'bold'),
                                       fill='black')  # 按钮显示文本
        canvas_.bind('<Button-1>', win_bind_1)  # 关联鼠标点击事件
        canvas_.bind('<Motion>', win_bind_2)  # 关联鼠标经过事件
        win.mainloop()

        '-----------------------------------------------------------------------------------------'
    elif 340 <= event.x <= 475 and 450 <= event.y <= 495:  # 响应的位置
        click_voice()
        Cancel = messagebox.askyesno('操作提示', '是否要退出程序?')
        if Cancel:
            root.destroy()
            pygame.mixer.music.stop()
            winsound.PlaySound('assets/sound/bye.wav', winsound.SND_LOOP)
            root.quit()




    elif 340 <= event.x <= 475 and 530 <= event.y <= 575:  # 响应的位置
        click_voice()
        win = Toplevel(root)
        win.grab_set()  # 阻止主界面和其他窗口的交互
        # 加载图像
        win.attributes("-alpha", 0.9)
        win.title('关于我                                                         (左/右键切换二维码)')
        win.iconbitmap("assets/img/personal.ico")
        width = 500
        height = 200
        size = Gui(width, height)
        win.geometry(size)
        win.resizable(width=False, height=False)
        wechat_image = Image.open('assets/img/wechat.jpg')
        wechat_photo = ImageTk.PhotoImage(wechat_image)
        wechat_label_text = Label(win, font=('方正姚体', 14), fg='#232526', text='扫描下方QQ二维码,联系我吧！')
        wechat_label_text.place(x=125, y=5)
        # 添加图像到标签
        wechat_photo_img = Label(win, image=wechat_photo)
        wechat_photo_img.place(x=175, y=30)
        qq_image = Image.open('assets/img/qq.jpg')
        qq_photo = ImageTk.PhotoImage(qq_image)
        # 添加图像到标签
        qq_photo_img = Label(win, image=qq_photo)
        qq_photo_img.place(x=500 + 250, y=30)
        # 背景切换
        win.bind('<Button-1>', lambda x: fluent_change(0))  # 鼠标左键切换界面
        win.bind('<Button-3>', lambda x: fluent_change(91))  # 鼠标右键切换界面

        def fluent_change(i):
            if i < 90:
                wechat_photo_img.place(x=-width * sin(i * pi / 180) + 175)
                qq_photo_img.place(x=width - width * sin(i * pi / 180) + 175)
                win.after(10, fluent_change, i + 1)  # 10ms移动一次
                wechat_label_text.configure(text='扫描下方微信二维码,联系我吧！')
                wechat_label_text.place(x=width - width * sin(i * pi / 180) + 125)
            elif 91 <= i < 180:
                qq_photo_img.place(x=width - width * sin(i * pi / 180) + 175)
                wechat_photo_img.place(x=width - width * sin(i * pi / 180) - 325)
                win.after(10, fluent_change, i + 1)  # 10ms移动一次
                wechat_label_text.configure(text='扫描下方QQ二维码,联系我吧！')
                wechat_label_text.place(x=width - width * sin(i * pi / 180) - 375)

        win.mainloop()


def bind_2(event):  # 鼠标经过响应函数
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:  # 响应的位置
        canvas.itemconfigure(start_out_frame, outline='black')  # 重设外框颜色
        canvas.itemconfigure(start_liner_frame, outline='black')  # 重设内框颜色
        canvas.itemconfigure(start_Text, fill='white')  # 重设显示文本颜色
        canvas.configure(cursor='hand2')  # 重设鼠标样式
    elif 340 <= event.x <= 475 and 450 <= event.y <= 495:  # 响应的位置
        canvas.itemconfigure(exit_out_frame, outline='black')  # 重设外框颜色
        canvas.itemconfigure(exit_liner_frame, outline='black')  # 重设内框颜色
        canvas.itemconfigure(exit_Text, fill='white')  # 重设显示文本颜色
        canvas.configure(cursor='hand2')  # 重设鼠标样式
    elif 340 <= event.x <= 475 and 530 <= event.y <= 575:  # 响应的位置
        canvas.itemconfigure(about_out_frame, outline='black')  # 重设外框颜色
        canvas.itemconfigure(about_liner_frame, outline='black')  # 重设内框颜色
        canvas.itemconfigure(about_Text, fill='white')  # 重设显示文本颜色
        canvas.configure(cursor='hand2')  # 重设鼠标样式
    else:
        canvas.itemconfigure(start_out_frame, outline='yellow')  # 恢复外框默认颜色
        canvas.itemconfigure(start_liner_frame, outline='yellow')  # 恢复内框默认颜色
        canvas.itemconfigure(start_Text, fill='red')  # 恢复显示文本默认颜色
        canvas.itemconfigure(exit_out_frame, outline='yellow')  # 恢复外框默认颜色
        canvas.itemconfigure(exit_liner_frame, outline='yellow')  # 恢复内框默认颜色
        canvas.itemconfigure(exit_Text, fill='red')  # 恢复显示文本默认颜色
        canvas.itemconfigure(about_out_frame, outline='yellow')  # 重设外框颜色
        canvas.itemconfigure(about_liner_frame, outline='yellow')  # 重设内框颜色
        canvas.itemconfigure(about_Text, fill='red')  # 重设显示文本颜色
        canvas.configure(cursor='arrow')  # 恢复鼠标样式


def Gui(width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2
    size = f'{width}x{height}+{int(x)}+{int(y)}'
    return size


def rectangle(x1, y1, x2, y2, style):
    return canvas.create_rectangle(x1, y1, x2, y2, outline=style)


# 暂停背景音乐
def pause_music():
    pygame.mixer.music.pause()


# 继续播放背景音乐
def unpause_music():
    pygame.mixer.music.unpause()


# 点击音效
def click_voice():
    winsound.PlaySound('assets/sound/change.wav', winsound.SND_ASYNC)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("assets/sound/bgm.mp3")
    pygame.mixer.music.play(-1)  # -1表示循环播放
    data = os.listdir('assets/skin/')
    is_run = False
    flag = True
    hero_flag = False
    info_flag = False
    counter = 0
    root = Tk()
    width = 800
    height = 600
    root.resizable(width=False, height=False)
    size = Gui(width, height)
    root.geometry(size)
    root.title('王者荣耀抽奖系统 --Version 1.0 by@Klock')
    root.iconbitmap("assets/img/logo.ico")
    # -------------------------分割线-----------------------#
    # 设置背景图   大小997x748
    bg = PhotoImage(file="assets/img/bg.png")
    canvas = Canvas(root, width=width, height=height, bd=0)
    canvas.create_image(width // 2, height // 2, anchor='center', image=bg)
    canvas.place(width=800, height=600)  # 设置Canvas控件大小及位置
    # -------------------------分割线-----------------------#
    x1, y1, x2, y2 = 340, 370, 475, 415
    font = ('楷体', 20, 'bold')
    fill = 'red'
    style = 'yellow'
    start_out_frame = rectangle(x1, y1, x2, y2, style)  # 按钮外框
    start_liner_frame = rectangle(x1 + 5, y1 + 5, x2 - 5, y2 - 5, style)  # 按钮内框
    start_text_x, start_text_y = round((x1 + x2) / 2), round((y1 + y2) / 2)
    start_Text = canvas.create_text(start_text_x, start_text_y, text='开 始', font=font, fill=fill)  # 按钮显示文本
    exit_out_frame = rectangle(340, 450, 475, 495, 'yellow')  # 按钮外框
    exit_liner_frame = rectangle(340 + 5, 450 + 5, 475 - 5, 495 - 5, style)  # 按钮内框
    exit_text_x, exit_text_y = round((340 + 475) / 2), round((450 + 495) / 2)
    exit_Text = canvas.create_text(exit_text_x, exit_text_y, text='退 出', font=font, fill=fill)  # 按钮显示文本
    about_out_frame = rectangle(340, 530, 475, 575, style)  # 按钮外框
    about_liner_frame = rectangle(340 + 5, 530 + 5, 475 - 5, 575 - 5, style)  # 按钮内框
    about_text_x, about_text_y = round((340 + 475) / 2), round((530 + 575) / 2)
    about_Text = canvas.create_text(about_text_x, about_text_y, text='关 于', font=font, fill=fill)  # 按钮显示文本
    # 导入图片并添加按钮
    start_ = ImageTk.PhotoImage(file="assets/img/pause.png")
    stop_ = ImageTk.PhotoImage(file="assets/img/start.png")
    start_music = Button(root, image=stop_, bg='#2A2835', command=unpause_music, relief="flat")
    stop_music = Button(root, image=start_, bg='#2A2835', command=pause_music, relief="flat")
    stop_music.place(x=726, y=96)
    start_music.place(x=726, y=6)
    canvas.bind('<Button-1>', bind_1)  # 关联鼠标点击事件
    canvas.bind('<Motion>', bind_2)  # 关联鼠标经过事件
    root.mainloop()
    pygame.mixer.music.stop()
    pygame.quit()
