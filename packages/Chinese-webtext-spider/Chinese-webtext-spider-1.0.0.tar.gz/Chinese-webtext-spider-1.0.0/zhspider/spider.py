import requests
import json
import time
import os
import time
import json
import urllib
from evaluator import Evaluator
from extractor import Extractor



class Spider:

    

    def __init__(self, database_path, sleep_time=15, mode="external", debug=True, load_old=False):
        self.database_path = database_path
        #folder = os.path.exists(self.database_path)
        self.sleep_time = sleep_time
        self.mode= mode
        self.debug = debug
        self.urls = {}
        self.visited_urls = {}
        self.docs = {}  #Dict[str,Dict[str,list[str]]] i.e. {域名:{url:文本列表}}
        self.last_get_html_time=0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
        }
        #创建原始路径
        if not os.path.exists(self.database_path):     
            os.makedirs(self.database_path)

        #导入urls库数据
        # url_database_database_path=self.database_path+'url_database/database/'
        # if  os.path.exists(url_database_database_path):     
        #     filelist = os.listdir(url_database_database_path)
        #     for filename in filelist:
        #         # print(filename)
        #         filename=filename[:-4]
        #         if filename not in self.urls:
        #             self.urls[filename] = []
        #         with open (url_database_database_path+filename +'.txt','r',encoding='utf-8') as file:
        #             content=file.readlines()
        #             for line in content:
        #                 if line not in self.urls[filename]:
        #                     self.urls[filename].append(line.strip('\n'))

        if load_old:
            #导入visited_urls
            if os.path.exists(os.path.join(database_path,'visited_urls.json.old')):
                with open(os.path.join(database_path,'visited_urls.json.old')) as f_obj:
                    self.visited_urls = json.load(f_obj)
            #导入urls
            if os.path.exists(os.path.join(database_path,'urls.json.old')):
                with open(os.path.join(database_path,'urls.json.old')) as f_obj:
                    self.urls = json.load(f_obj)
            #导入visited_urls
            if os.path.exists(os.path.join(database_path,'docs.json.old')):
                with open(os.path.join(database_path,'docs.json.old')) as f_obj:
                    self.docs = json.load(f_obj)           
        else:
            #导入visited_urls
            if os.path.exists(os.path.join(database_path,'visited_urls.json')):
                with open(os.path.join(database_path,'visited_urls.json')) as f_obj:
                    self.visited_urls = json.load(f_obj)
            #导入urls
            if os.path.exists(os.path.join(database_path,'urls.json')):
                with open(os.path.join(database_path,'urls.json')) as f_obj:
                    self.urls = json.load(f_obj)
            #导入visited_urls
            if os.path.exists(os.path.join(database_path,'docs.json')):
                with open(os.path.join(database_path,'docs.json')) as f_obj:
                    self.docs = json.load(f_obj)
       
       

        # #导入doc数据库
        # text_database_database_path=self.database_path+'text_database/database/'
        # if  os.path.exists(text_database_database_path):     
        #     filelist = os.listdir(text_database_database_path)
        #     for filename in filelist:
        #         with open (text_database_database_path+filename,'r',encoding='utf-8') as file:
        #             lines=file.readlines()
        #             for line in lines:
        #                 content=line.split('<eod><bod>')
        #                 url=content[0].split('<bod>')[0].split('<bop>')[1]
        #                 content[0]=content[0].split('<bod>')[1]
        #                 content[-1]=content[-1].split('<eod>')[0]
        #                 self.docs[url] = content

    def other_rule(self,url):
        return True
    
    def ban(self, url):
        return False

    def is_valid(self, url):
        is_pure_url = '#' not in url and '?' not in url and '=' not in url and '%' not in url and '+' not in url and '&' not in url and ' ' not in url 
        is_normal_domain = '.com' in url or '.net' in url
        is_link = 'js' not in url and 'css' not in url and 'png' not in url and 'jpg' not in url and 'htm'not in url
        is_content = 'gov' not in url and 'edu' not in url 
        return is_pure_url and is_normal_domain and is_link and is_content 
    
    def add_url(self, url, force=True):
        """
            默认外部添加的url是合法的
        """

        if self.ban(url):
            return

        # print("add:",url)
        domain = self.get_domain(url)
        if force:
            if domain not in self.urls:
                self.urls[domain] = []

            if domain not in self.visited_urls:
                self.visited_urls[domain] = []
                
            if url not in self.urls[domain]:
                if 'https' in url:
                    if 'http'+url[5:] not in self.urls[domain] and 'http'+url[5:] not in self.visited_urls[domain]:
                        self.urls[domain].append(url) 
                elif 'http' in url:
                    if 'https'+url[4:] not in self.urls[domain] and 'https'+url[4:] not in self.visited_urls[domain]:
                        self.urls[domain].append(url) 

        elif self.is_valid(url):
            if self.mode == "external" or (self.mode == "inner" and domain in self.urls):
                if domain not in self.urls:
                    self.urls[domain] = []
                if domain not in self.visited_urls:
                    self.visited_urls[domain] = []
                if url not in self.urls[domain]:
                    if 'https' in url:
                        if 'http'+url[5:] not in self.urls[domain] and 'http'+url[5:] not in self.visited_urls[domain]:
                            self.urls[domain].append(url) 
                    elif 'http' in url:
                        if 'https'+url[4:] not in self.urls[domain] and 'https'+url[4:] not in self.visited_urls[domain]:
                            self.urls[domain].append(url)             
         
        

    def get_urls(self):
        return_urls = []
        for domain, links in self.urls.items():
            if domain not in self.visited_urls:
                self.visited_urls[domain]=[]
            # print("wai:",links)
            # print("bool:",bool(links))
            while links:
                link = links.pop()
                # print("内:",links)
                # print(self.urls[domain])
                if link not in self.visited_urls[domain]: 
                    self.visited_urls[domain].append(link)
                    return_urls.append(link)
                    break
        return return_urls

    def pick_webtext(self, html):
        """
        return List[str] : cherry-pick webtext you want get in html
        """
        extractor=Extractor()
        return extractor.extract_text(html)


    def crawl(self):
        extractor=Extractor()
        while 1:
            geted_urls=self.get_urls()
            if len(geted_urls) == 0:
                self.save()
                break
            
            for url in geted_urls:
                # print('爬取：',url)
                html=self.get_html(url)
                # print(html)
                need_add_urls=extractor.extract_url(html)
                # print("need:",need_add_urls)
                for need_add_url in need_add_urls:
                    self.add_url(need_add_url,force=False)
                
                if self.other_rule(url):
                    cleaned_texts = self.pick_webtext(html) #list[str]
                    if not cleaned_texts:
                        continue
                    domain = self.get_domain(url)
                    if domain not in self.docs:
                        self.docs[domain]={}
                    self.docs[domain][url]=cleaned_texts
                    
            self.save()
            time.sleep(self.sleep_time)


        

    def get_html(self, url: str) :
        


        try:
            r = requests.get(url, headers=self.headers, timeout=15)
        except:
            return ""
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
        else:
            return ""

    # def deduplicate(self,test_doc:str ) :#判断相似性
    #     evaluator = Evaluator()
    #     for domain,doc in self.docs.items():
    #         if evaluator.predict(test_doc,doc)>0.7:
    #             return 1
    #     return 0

                    
    def save(self) :
        # #url数据库路径创建
        # url_database_path = self.database_path+'url_database/'
        # url_website_path =url_database_path+'website.txt'
        # url_database_database_path=url_database_path+'database/'
        # #folder1 = os.path.exists(url_database_path)
        # if not os.path.exists(url_database_path):     
        #     os.makedirs(url_database_path)
        # #folder2 = os.path.exists(url_database_database_path)
        # if not os.path.exists(url_database_database_path):     
        #     os.makedirs(url_database_database_path)

        # #text数据库路径创建
        # text_database_path = self.database_path+'text_database/'
        # text_website_path =text_database_path+'website.txt'
        # text_database_database_path=text_database_path+'database/'
        
        # if not os.path.exists(text_database_path):     
        #     os.makedirs(text_database_path)
        
        # if not os.path.exists(text_database_database_path):     
        #     os.makedirs(text_database_database_path)

        # #写入url数据库
        # print('写入url数据库')
        # with open(url_website_path,"w") as f:
        #     for domain in self.urls:
        #         f.write(domain+'\n')

        # for domain in self.urls:
        #     with open(url_database_database_path+'/'+domain+'.txt',"w") as f:
        #         for url in self.urls [domain]:               
        #             f.write(url+'\n')

        # #写入doc数据
        # print('写入doc数据库')
        # with open(text_website_path,"w") as f:
        #     for url in self.docs:
        #         domain=self.get_domain(url)
        #         f.write(domain+'\n')

        # for url in self.docs:
        #     domain=self.get_domain(url)
        #     with open(text_database_database_path+'/'+domain+'.txt',"w") as f:
        #         f.write('<bop>'+url)
        #         for doc in self.docs[url]:   
        #             print('**')
        #             print(doc)   
        #             print(type(doc))         
        #             f.write('<bod>'+doc+'<eod>')
        #         f.write('<eop>\n')

        #保存visited_urls
        # print('保存json')

        file_name = os.path.join(self.database_path,'visited_urls.json')
        if os.path.exists(file_name):
            if os.path.exists(file_name+'.old'):
                os.unlink(file_name+'.old')         
            os.rename(file_name,file_name+'.old')

        file_name = os.path.join(self.database_path,'urls.json')
        if os.path.exists(file_name):
            if os.path.exists(file_name+'.old'):
                os.unlink(file_name+'.old')
            os.rename(file_name,file_name+'.old')

        file_name = os.path.join(self.database_path,'docs.json')
        if os.path.exists(file_name):
            if os.path.exists(file_name+'.old'):
                os.unlink(file_name+'.old')
            os.rename(file_name,file_name+'.old') 

        with open(os.path.join(self.database_path,'visited_urls.json'), 'w') as f_obj:
            json.dump(self.visited_urls, f_obj, ensure_ascii=False)
        
        with open(os.path.join(self.database_path,'urls.json'), 'w') as f_obj:
            json.dump(self.urls, f_obj, ensure_ascii=False)
        
        with open(os.path.join(self.database_path,'docs.json'), 'w') as f_obj:        
            json.dump(self.docs, f_obj, ensure_ascii=False)
         
                

    def get_domain(self, url: str) :
        return urllib.parse.urlparse(url).netloc
