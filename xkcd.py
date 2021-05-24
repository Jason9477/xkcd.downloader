import os                    #有寫網頁有多個圖片,沒有圖片,標籤不同真的很煩
import random
import sys
from bs4 import BeautifulSoup
import requests
from PIL import Image
if len(sys.argv)==2:
    if str(sys.argv[1]) == 'help':
        print('I need help')
        print('用法：python xkcd.py [功能] ([模式] [要下載的範圍])')
        print('ex:python3 xkcd.py 1')
        print('ex:python3 xkcd.py 2 r')
        print('ex:python3 xkcd.py 2 1-5')
        print('ex:python3 xkcd.py 2 1,2,3,4,5')
        print('ex:python3 xkcd.py 2 1')
        print('ex:python3 xkcd.py 2 in_your_classroom')
        print('xkcd.com 是一個很酷的漫畫網站，從 2005 年開始，網站上上面會不定期刊載作者 Randall Munroe 繪製的漫畫，經常以火柴形狀的人物呈現許多生活中不同主題的梗或趣味話題。\n')
        print('輸入1大量下載：一次下載任意 50 張 xkcd 的漫畫（不限哪幾張但不可重複）。先建立一個資料夾（子目錄），之後將這 50 張全部存成個別的檔案置入資料夾中。\n')
        print('===================================================================================================================================')
        print('功能2指定下載：以 input 輸入指定的漫畫，下載存入一個 png，並且打開。')
        print('功能二的模式：')
        print("    輸入單一數字，代表下載一則。")
        print("    輸入 r 和 random 代表隨機下載一則。")
        print("    輸入以 , 分隔的多個數字，代表下載多則。")
        print("    輸入一個 數字-數字 的範圍，代表下載多則。")
        print("    輸入名稱下載一則")
        quit()
if len(sys.argv)==1:
    print('xkcd.com 是一個很酷的漫畫網站，從 2005 年開始，網站上上面會不定期刊載作者 Randall Munroe 繪製的漫畫，經常以火柴形狀的人物呈現許多生活中不同主題的梗或趣味話題。\n')
    print('輸入1大量下載：一次下載任意 50 張 xkcd 的漫畫（不限哪幾張但不可重複）。先建立一個資料夾（子目錄），之後將這 50 張全部存成個別的檔案置入資料夾中。\n')
    print('輸入2指定下載：以 input 輸入指定的漫畫，下載存入一個 png，並且打開。')
a = 2466
s = 'https://xkcd.com/'
urlst = []
for _ in range(1, 2467):
    urlst.append(s+str(_))
while 1:  # 偵測新漫畫
    res = requests.get(s+str(a))
    res = str(res)
    a += 1
    if '200' in res:
        urlst.append(s+str(a))
    else:
        break
if len(sys.argv)==1:
    n = int(input())
else:
    n=int(sys.argv[1])
if n == 1:  # 第一項操作
    os.mkdir('./xkcd')
    new_url = urlst
    random.shuffle(new_url)
    for i in range(50):


        r = requests.get(new_url[i])
        soup = BeautifulSoup(r.text, "html.parser")
        result = soup.select('#comic > img')
        if result == []:
            result = soup.select('#comic > a > img')
        re = 'https:'+result[0].attrs['src']
        res = requests.get(re)
        re = re.split('/')[-1]
        re = re.split('.')[0]
        with open('xkcd/'+re+'.png', 'wb') as f:
            f.write(res.content)

if n == 2:  # 第二項操作
    if len(sys.argv)==1:
        print("輸入單一數字，代表下載一則。")
        print("輸入 r 和 random 代表隨機下載一則。")
        print("輸入以 , 分隔的多個數字，代表下載多則。")
        print("輸入一個 數字-數字 的範圍，代表下載多則。")
        print("輸入名稱下載一則")
    FLAG = True
    while FLAG is True:
        if len(sys.argv)==1:
            op = input()
        else:
            op=sys.argv[2]
        if op == 'random' or op == 'r':  # random
            FLAG = False
            res = random.choice(urlst)
            r = requests.get(res)
            soup = BeautifulSoup(r.text, "html.parser")
            result = soup.select('#comic > img')
            if result == []:
                result = soup.select('#comic > a > img')
            re = 'https:'+result[0].attrs['src']
            res = requests.get(re)
            re = re.split('/')[-1]
            re = re.split('.')[0]
            with open(re+'.png', 'wb') as f:
                f.write(res.content)
            Image.open(re+".png").show()
            break

        elif ',' in op:  # number,number...
            FLAG = False
            multilist = op.split(',')
            multilist.remove('')
            for i in multilist:
                if int(i) > a or int(i) <= 0:
                    print('無此漫畫，請重新輸入')
                    if len(sys.argv)!=1:
                        quit()
                    FLAG = True
                    break
                else:
                    pass

            if FLAG is not True:
                for i in multilist:
                    r = requests.get(s+i)
                    soup = BeautifulSoup(r.text, "html.parser")
                    result = soup.select('#comic > img')
                    if result == []:
                        result = soup.select('#comic > a > img')
                    re = 'https:'+result[0].attrs['src']
                    res = requests.get(re)
                    re = re.split('/')[-1]
                    re = re.split('.')[0]
                    with open(re+'.png', 'wb') as f:
                        f.write(res.content)
                    Image.open(re+".png").show()

        elif '-' in op:  # number-nuber
            multilist = list(map(int, op.split('-')))
            if multilist[0] > a or multilist[0] <= 0 or multilist[1] > a or multilist[1] <= 0:
                print('無此漫畫，請重新輸入')
                if len(sys.argv)!=1:
                    quit()
                FLAG = True
                continue
            else:
                lst = []
                FLAG = False
                for _ in range(multilist[0], multilist[1]+1):
                    lst.append(str(_))
                for i in lst:
                    r = requests.get(s+i)
                    soup = BeautifulSoup(r.text, "html.parser")
                    result = soup.select('#comic > img')
                    if result == []:
                        result = soup.select('#comic > a > img')
                    re = 'https:'+result[0].attrs['src']
                    res = requests.get(re)
                    re = re.split('/')[-1]
                    re = re.split('.')[0]
                    with open(re+'.png', 'wb') as f:
                        f.write(res.content)
                    Image.open(re+".png").show()

        elif op.isdigit():  # 輸入編號
            if int(op) > a or int(op) <= 0:
                print('無此漫畫，請重新輸入')
                if len(sys.argv)!=1:
                    quit()
                FLAG = True
                continue
            else:
                FLAG = False
                r = requests.get(s+op)
                soup = BeautifulSoup(r.text, "html.parser")
                result = soup.select('#comic > img')
                if result == []:
                    result = soup.select('#comic > a > img')
                re = 'https:'+result[0].attrs['src']
                res = requests.get(re)
                re = re.split('/')[-1]
                re = re.split('.')[0]
                with open(re+'.png', 'wb') as f:
                    f.write(res.content)
                Image.open(re+".png").show()
        else:  # 輸入名稱
            #print('op in bonus!!!!!')
            FLAG = False
            res = requests.get('https://imgs.xkcd.com/comics/'+op+'.png')
            if '200' not in str(res):
                res = requests.get('https://imgs.xkcd.com/comics'+op+'.jpg')
            with open(op+'.png', 'wb') as f:
                f.write(res.content)

            Image.open(op+".png").show()
