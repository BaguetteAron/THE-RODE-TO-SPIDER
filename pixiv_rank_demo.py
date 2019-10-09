import requests
from bs4 import BeautifulSoup
import os
import time
import datetime
import threading
import sys
import io
#from selenium import webdriver 被弃用的selenium方法，加载元素使得爬取效率过慢
#本爬虫需要自行翻墙

rem=requests.Session()
exitflag = 0
starttime = datetime.datetime.now()
localtime=time.strftime('%Y%m%d',time.localtime(time.time()))

base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
main_url = 'http://www.pixiv.net'
headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'referer':'https://accounts.pixiv.net/login',
        'origin': 'https://accounts.pixiv.net',
        'cookie':'   
        }
 


#def login():
#    pixiv_id=""
#    password="
#    post_key=[]
#    return_to = 'http://www.pixiv.net/'
#    ip_list = []
#    post_key_html = rem.get(base_url, headers=headers)
#    post_key_htmll = post_key_html.text
#    post_key_soup = BeautifulSoup(post_key_htmll, 'lxml')
#    post_key=post_key_soup.find('input')['value']
#    data = {
#            'pixiv_id': pixiv_id,
#            'password': password,
#            'return_to': return_to,
#            'post_key': post_key
#                }
#    lo=rem.post(login_url, data=data, headers=headers)
##模拟登录，p站模拟登录需要获取一下post_key
#卡在谷歌验证码

def get_ssearch(s_name):
    search_url='https://www.pixiv.net/search.php?s_mode=s_tag&word='+s_name

#挖坑搜索功能








##需要的排行榜时间
def get_time(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date,"%Y%m%d")
    end_date = datetime.datetime.strptime(end_date,"%Y%m%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days = 1)
    return date_list

#获取前十名图片
def get_ss(used_date):
    url="https://www.pixiv.net/ranking.php?mode=daily"
    main_url = 'http://www.pixiv.net'
    if used_date!=localtime:
        url=url+'&date='+used_date

    li_html=rem.get(url,headers=headers).text
    li_soup = BeautifulSoup(li_html, 'lxml')
    ss=li_soup.find_all("section",{'class':"ranking-item"})
    ss=ss[0:9]

    return ss
#获取图片资源
def get_src(i):
    src=i.find("img")["data-src"]
    #关于处理漫画思路之一 判断将p0改为p1是否可以访问
    src=src.replace(src.split('/')[3],'').replace(src.split('/')[4],'').replace(src.split('/')[5],'img-original').replace(src.split('_')[-1],'.jpg')
    
    src=src.split("_")[0]+"_"+src.split("_")[1]+src.split("_")[-1]
    test=rem.get(src,headers=headers)
    code=test.status_code
    if code!=200:
        src=src.replace(".jpg",".png")
    return src

def get_name(i):
        #获取图片大小
    img_n=i.get("data-title")
    return img_n

def get_size(src,img_n):
        image = rem.get(src,headers=headers)
        imagea=image.content
        image_b = io.BytesIO(imagea).read()
        size = len(image_b)
        print('\n')
        print("*图片名：{}\n*{} kb".format(img_n, size / 1e3))

        return size
    
       
    #下载
def download(src,img_n,total_size):
    title = img_n.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_')\
                .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
    root = 'e://pics//test//'+used_date+"//"
    path = root + title+'.'+src.split('.')[-1]
    filename=path
    data_count=0
    content_size=total_size
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r =rem.get(src, headers=headers)
            r.encoding = r.apparent_encoding
            with open(path,'ab') as code:
                for chunk in r.iter_content(chunk_size=2048): #边下载边存硬盘（便于显示进度
                    if chunk:
                        code.write(chunk)
                        start_time=time.time()
                        while data_count<content_size:
                            time.sleep(0.005)
                            if os.path.exists(filename):
                               data_count = data_count + len(chunk)
                               down_rate=(os.path.getsize(filename)-data_count)/1024/1024
                               print (" "+str('%.2f' %(down_rate/(time.time() - start_time))+"MB/s"),end="")                            
                        
                            rate = data_count/content_size
                            rate_num = int(rate * 100)
                            number=int(50*rate)
                            r = '\r[%s%s]%d%%' % ("*"*number, " "*(50-number), rate_num, )
                            print("\r {}".format(r),end=" ")
                   
                        now_jd = (data_count / content_size) * 100
                        print("\r 文件下载进度：%d%%" % (now_jd), end=" ")
    

                    else:
                        break  
            print("\n{} has finished".format(img_n))        
        else:
            print("{}图片已存在".format(img_n))
    except:
        print("{}...error".format(img_n))
    time.sleep(3)
        #多线程
def work_top(used_date):
    ss=get_ss(used_date)
    for i in ss:
        src=get_src(i)
        img_n=get_name(i)
        total_size=get_size(src,img_n)
        download(src,img_n,total_size)
    print('{} has finished'.format(used_date))

class myThread(threading.Thread):

    def __init__(self, threadID, name, list):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.list = list

   
        
    def run(self):
        print("启动线程编号：" + self.name)
        # threadLock.acquire()
        get_img(self.name, self.list)
        # threadLock.release()
        print("退出线程："+ self.name)


def get_img(threadname, list):
    if len(list):
        for used_date in list:
            
            if exitflag:
                threadname.exit()
            work(used_date)
if __name__ == '__main__':
    #functions = {1: '**二次元の世界三次元勿入哦~~~~~~~~',
    #         2: '**小可爱你再确认下~你全家真的不都是二次元吗？',
    #         3: '**三次元のhentai！下次就gck哦！'}


    #for i in range(1,5):
    #    print("**你是二次元吗？你全家都是二次元吗？\n")
    #    answer=input()
    #    print('\n')
    #    if(answer=='YES'or answer=='yes'or answer=='是' or answer=='您说是，辣就是'):
    #        print('**欢迎来到二次元的后花园哦~~~\n')
    #        break
    #    else:
    #        if(i==4):
    #            os._exit(0)
    #        else:
    #            print(functions[i])
    #            print('\n**呐~我在问一次哦~~\n')
         
    print('**pixiv爬虫启动！')       
    print('**请输入开始时间:')
    begin_date=input()
    print('**请输入结束时间:')
    end_date=input()
    date_list=get_time(begin_date,end_date)

    list1 = []
    list2 = []
    list3 = []
    for used_date,i in zip(date_list,range(0,1000)):
        if i % 3 == 0:
            list1.append(used_date)
        if i % 3 == 1:
            list2.append(used_date)
        if i % 3 == 2:
            list3.append(used_date)
    threads = []
    thread1 = myThread(1, "thread-1", list1)
    thread2 = myThread(2, "thread-2", list2)
    thread3 = myThread(3, "thread-3", list3)
    thread1.start()
   
    thread2.start()
   
    thread3.start()
   
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    for t in threads:
        t.join()
    print("退出主线程")
    endtime = datetime.datetime.now()
 
    print (endtime - starttime)

    



   

 
