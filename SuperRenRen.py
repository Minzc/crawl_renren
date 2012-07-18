# coding=gb2312
import urllib, urllib2, cookielib, json, time, md5, re
from bs4 import BeautifulSoup
class RenRen:
    def __init__(self,email,password):
        self.email = email
        self.password = password
        #LWPCookie ���������Ӳ�̴��cookieҲ���Լ���Ӳ���м���cookie
        #����һ��cookie��������
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert("renren.cookie")
        except:
            print "������������cookie"        
        #��HTML�ļ���ʱ�ö��󽫴���cookies������build_opener���Խ�����������������
        #(��Щ���򽫰������Ǳ�ָ����˳��������һ��)��Ϊ����������һ����
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))        
        #�������urlopen()ʹ��opener��������HTML�ļ��Ļ������Ե���install_opener
        #(opener)����������opener���󴫸�����������ʹ��opener�����open(url)��������HTML�ļ�
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
        #��̰��ƥ��
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
                    #���ص���һ��unicode����,ʹ��unicode�����encode����ת��
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
                            print name,"��ȡͼƬ����"
                            file.write(name+"��ȡͼƬ����\n")
                            err += 1
                    except:
                        print name,"ƥ��url����"
                        file.write(name+"ƥ��url����\n")
                        err += 1
            print "�Ѿ�������",i,'/',len(friends),'�û�,����',err,'��'

#                          
if __name__ == '__main__':
    r = RenRen('405681240@qq.com','5636595')
    r.login()
    r.friends()