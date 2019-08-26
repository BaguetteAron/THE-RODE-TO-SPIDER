import requests
from bs4 import BeautifulSoup
import os
import time
#from selenium import webdriver 被弃用的selenium方法，加载元素使得爬取效率过慢

#模拟登录
base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
main_url = 'http://www.pixiv.net'
headers={
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 75.0.3770.142Safari / 537.36',
        'Referer':'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        #p站爬取高清图需要referer
        'cookie':""
        #爬取r18图需要用到cookie(有了cookie还需要模拟登录？）
        }
 
pixiv_id="" #p站登陆信息 爬原图需要登陆
password=""
post_key=[]
return_to = 'http://www.pixiv.net/'
ip_list = []
post_key_html = requests.get(base_url, headers=headers).text
post_key_soup = BeautifulSoup(post_key_html, 'lxml')
post_key=post_key_soup.find('input')['value']
data = {
        'pixiv_id': pixiv_id,
        'password': password,
        'return_to': return_to,
        'post_key': post_key
            }
requests.post(login_url, data=data, headers=headers)
#模拟登录，p站模拟登录需要获取一下post_key


main_url = 'http://www.pixiv.net'
url="https://www.pixiv.net/ranking.php?mode=daily_r18"  #排行榜的链接
li_html=requests.get(url,headers=headers).text
li_soup = BeautifulSoup(li_html, 'lxml')
ss=li_soup.find_all("section",{'class':"ranking-item"})

for i in ss:
    src=i.find("img")["data-src"] #获取缩略图的地址
        #将缩略图的地址稍作修改可以转换成原图地址
    src=src.replace(src.split('/')[3],'').replace(src.split('/')[4],'').replace(src.split('/')[5],'img-original').replace(src.split('_')[-1],'.jpg')
    src=src.split("_")[0]+"_"+src.split("_")[1]+src.split("_")[-1]
        #通过是否正常访问判断原图是否是jpg格式
    test=requests.get(src,headers=headers)
    code=test.status_code
    if code!=200:
        src=src.replace(".jpg",".png")

   #jump_to_url =main_url + href
   #driver=webdriver.chrome()   #声明浏览器对象
   #driver.set_page_load_timeout(20)
  
   #try:
   #    driver.get(jump_to_url)
   #except:
   #    driver.execute_script("window.stop()")
   #html = driver.page_source
   #driver.quit()#关闭浏览器
   #img_soup = beautifulsoup(html, 'html5lib')
   #img_src=img_soup.find_all('a',{'class':"sc-lznbd ffeuqj"}) 
   #try:
   #    img_href=img_src[0].get('href')
   #except:
   #    print("error")
   #img_name=[]
   #img_name=img_soup.find_all('img',{"class":"sc-lznbb jreise"}) #原seleum方法

        
    img_n=i.get("data-title")   #获取名字
    print("{}....正在下载中_(:з」∠)_..........".format(img_n))
        #替换掉不能作为系统文件名字的字符
    title = img_n.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_')\
             .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
    root = 'e://pics//r18//' #路径
    path = root + title+'.'+src.split('.')[-1]
   
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(src, headers=headers)
            r.encoding = r.apparent_encoding
            with open(path,'wb') as f:
                f.write(r.content)
            f.close()
            print("finished")          
        else:
            print("图片已存在")
    except:
        print("error")

    
    time.sleep(4) #防止爬的太快

