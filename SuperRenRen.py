# coding=gb2312
import urllib, urllib2, cookielib, json, time, md5, re
from bs4 import BeautifulSoup
class RenRen:
    def __init__(self,email,password):
        self.email = email
        self.password = password
        #LWPCookie 对象可以向硬盘存放cookie也可以加载硬盘中加载cookie
        #设置一个cookie操作对象
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert("renren.cookie")
        except:
            print "不能重新载入cookie"        
        #当HTML文件打开时该对象将处理cookies。函数build_opener可以接收零个或多个处理程序
        #(这些程序将按照它们被指定的顺序连接在一起)作为参数并返回一个。
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))        
        #如果想让urlopen()使用opener对象来打开HTML文件的话，可以调用install_opener
        #(opener)函数，并将opener对象传给它。否则，请使用opener对象的open(url)函数来打开HTML文件
        urllib2.install_opener(self.opener)

    def login(self):
        params = {'email':self.email,'password':self.password}
        req = urllib2.Request('http://www.renren.com/PLogin.do',
                              urllib.urlencode(params))
        r = self.opener.open(req)
    def friends(self):
        req = 'http://friend.renren.com/myfriendlistx.do'
        r = self.opener.open(req)
        data = r.read()
        #非贪婪匹配
        f = re.search('friends=\[{.*?}\]',data).group()
        f = f[8:]
        f = f.replace('true','True').replace('false','False')
        friends = eval(f)
        print "number of friends",len(friends)
        i = 0
        err = 0
        file = open("log","w")
        for fd in friends:
            name = ""
            i += 1
            for key in fd.keys():
                if key == 'name':
                    #返回的是一个unicode对象,使用unicode对象的encode函数转码
                    name = eval("u'"+fd[key]+"'").encode('utf-8')
                if key == 'id':
                    req = "http://www.renren.com/profile.do?id="+str(fd[key])
                    r = self.opener.open(req)
                    data = r.read()
                    soup = BeautifulSoup(data)
                    try:
                        url = soup.findAll(id="userpic")[0]['src']
                        try:
                            imgReader = self.opener.open(url)
                            img = imgReader.read();
                            fileObj = open(name+".jpg","wb")
                            fileObj.write(img)
                        except:
                            print name,"读取图片出错"
                            file.write(name+"读取图片出错\n")
                            err += 1
                    except:
                        print name,"匹配url出错"
                        file.write(name+"匹配url出错\n")
                        err += 1
            print "已经处理了",i,'/',len(friends),'用户,错误',err,'人'

#                          
if __name__ == '__main__':
    r = RenRen('405681240@qq.com','5636595')
    r.login()
    r.friends()