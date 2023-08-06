from .spider import Spider
import re
from .evaluator import Evaluator
from .extractor import Extractor

class BilibiliSpider(Spider):
    def __init__(self, database_path, sleep_time=15, mode="external", debug=True, load_old=False):
        super().__init__(database_path, sleep_time, mode, debug, load_old)
        
        # 构造初始url
        # https://www.bilibili.com/read/cv22990000 从2023-04-11 16:27开始往前爬
        # https://www.bilibili.com/read/cv20000000 爬到2022-11-24 13:57 共5个月

        # 太慢了
        # for i in range(22990000,20000000,-1):
        #     print(i)
        #     if i%100000==0:
        #         print(i)
        #     self.add_url('https://www.bilibili.com/read/cv'+str(i))

        if 'www.bilibili.com' not in self.urls:
            self.urls['www.bilibili.com']=[]

        # 重置
        if len(self.urls['www.bilibili.com'])<10:
            self.urls['www.bilibili.com']=['https://www.bilibili.com/read/cv'+str(i) for i in range(20000000,22990001)]
            self.visited_urls={}
        

    # 只对满足other_rule的url的HTML进行提取文本(pick_webtext)
    def other_rule(self,url):
        return 'read' in url and "cv" in url
    
    # 被ban的url将不会访问
    def ban(self,url):
        return 'read' not in url
    
    def pick_webtext(self,html):
        threshold = 5
        if '页面不存在或已被删除' in html:
            return []
        
        if not html:
            return []

        # 获取点赞数
        upvote_re = r'like":[\s\S]*?"dislike"'
        upvote = re.findall(upvote_re,html)[0]
        upvote = re.findall(r'\d+',upvote)[0]           
        upvote = int(upvote)   
        # print(upvote)
        # print(html)

        if upvote < threshold:
            return []

        # 获取正文
        content_re = r'"content":"[\s\S]*?","keywords":"'
        content = re.findall(content_re,html)[0]

        content = re.sub(r'"content":"','',content)
        content = re.sub(r'","keywords":"','',content)


        # content = re.sub(r'{\\"ops\\":\[{\\"insert\\":\\"','',content)
        # content = re.sub(r'\\"}]}','',content)
        # content = content.strip(r'"content":"')
        # content = content.strip(r'","keywords":"')
        # content = content.strip(r'{\\"ops\\":[{\\"insert\\":\\"')
        # content = content.strip(r'\\"}]}')



        if r'\"insert\":\"' in content:
            reg = r'{\\"insert\\":\\"[\s\S]*?\\"}'
            content = re.findall(reg,content)
            str_list = []
            for c in content:
                # print(c)
                # print(c[14:-3])
                str_list.append(c[14:-3])
            content = '\n'.join(str_list)

        # print([content])
        

        # 删标签
        content = re.sub(r'</h\d>|</p>','\n',content)
        
        content = re.sub(r'\\u003C\\u002Fp\\u003E','\n',content)
        content = re.sub(r'\\u003c\\u002fp\\u003e','\n',content)
        content = re.sub(r'\\u003C\\u002Fh\d\\u003E','\n',content)
        content = re.sub(r'\\u003c\\u002fh\d\\u003e','\n',content)

        content = re.sub(r'\\u003Ch\d\\u003E','\n',content)
        content = re.sub(r'\\u003ch\d\\u003e','\n',content)
        content = re.sub(r'\\u003Cp\\u003E','\n',content)
        content = re.sub(r'\\u003cp\\u003e','\n',content)

        content = re.sub(r'<[^>]+>','',content)
        content = re.sub(r'\\u003C[\s\S]*?\\u003E','',content)
        content = re.sub(r'\\u003c[\s\S]*?\\u003e','',content)
        # print([content])
        # 把unicode转回str
        content = re.sub(r'\\u002F',r'/',content)
        content = re.sub(r'\\u002f',r'/',content)
        content = re.sub(r'\\u002C',r'<',content)
        content = re.sub(r'\\u002c',r'<',content)
        content = re.sub(r'\\u002E',r'>',content)
        content = re.sub(r'\\u002e',r'>',content)
        content = re.sub(r'\\\\n','\n',content)
        content = re.sub(r'\\\\t','\t',content)
        content = re.sub(r'\\\\\\"',r'"',content)
        content = re.sub(r'\\\\',r'\\',content)
        content = re.sub(r'\\n',r'\n',content)
        content = re.sub(r'\\t',r'\t',content)
        
        
        # html实体转回字符
        import html
        content = html.unescape(content)
        del html 

        # 删空行
        content = re.sub(r'\s*\n\s*','\n',content) 
        return [content.lstrip('\n')]
    
class CSDNSpider(Spider):
    def __init__(self, database_path, sleep_time=15, mode="external", debug=True, load_old=False):
        super().__init__(database_path, sleep_time, mode, debug, load_old)

    def other_rule(self,url):
        return 'article/details' in url
    def pick_webtext(self,html):
        threshold = 5
        
        if not html:
            return []
        # 获取点赞数
        upvote_re = r'<span id="spanCount" class="count ">[\s\S]*?</span>'
        upvote = re.findall(upvote_re,html)[0]
        upvote = re.findall(r'\d+',upvote)[0]           
        upvote = int(upvote)   
        # print(upvote)
        # print(html)

        if upvote < threshold:
            return []

        # 获取正文
        content_re = r'<article class="baidu_pl">[\s\S]*?</article>'
        content = re.findall(content_re,html)[0]

        # 分割代码
        content = re.split("(<code class=[\s\S]*?</code>)",content)

        return_texts = []
        for c in content:

            # 处理代码内容
            if "<code class=" in c:
                
                # 获取语言
                # r"""<code class="prism language-python">"""
                # print(c)
                language = c.split("""language-""")
                # print("debug:",len(language))
                if len(language) == 1:
                    language = "code"
                else:
                    language = language[1]
                language = language.split('\"')[0]
                # print(language)
                
                # 删标签
                c = re.sub(r'<[^>]+>','',c)

                # 将HTML实体转回字符
                import html
                c = html.unescape(c)
                del html

                # print("<"+language+">\n"+c+r"</"+language+">")
                # print('---'*40)

                return_texts.append("<"+language+">\n"+c+"\n</"+language+">")
            # 处理文本内容
            else:

                # 获取latex
                latex_re = r'(<span class="katex-mathml">[\s\S]*?</span>)'
                c_list = re.split(latex_re,c)

                
                for ind in range(len(c_list)):
                    # 提取latex
                    if r'<span class="katex-mathml">' in c_list[ind]:
                        c_list[ind] = re.sub(r'<span class="katex-mathml">','\n',c_list[ind])
                        # c_list[ind] = re.sub('\n\s','\n',c_list[ind])
                        # c_list[ind] = re.findall(r'[^\n]{30,}',c_list[ind])
                        c_list[ind] = c_list[ind].split('\n')

                        # latex表达式最长
                        c_list[ind] = sorted(c_list[ind],key=lambda x:-len(x))[0].strip()

                        # print([c_list[ind]])
                        # print('-'*40)
                    # 删除latex渲染
                    elif r'<span class="katex-html">' in c_list[ind]:
                        # print(c_list[ind])
                        c_list[ind] = re.sub(r'</h\d>|</p>|</br>|</title>|</li>|<br />','\n',c_list[ind])
                        c_list[ind] = c_list[ind].split('\n')[1:]
                        c_list[ind] = '\n'.join(c_list[ind])
                        # print(c_list[ind])
                        # print('-'*40)
                        
                     
                c = '\n'.join(c_list)
                # print(c) 
                # print('^^^'*40)

                # 删标签
                c = re.sub(r'</h\d>|</p>|</br>|</title>|</li>|<br />','\n',c)
                # print(c) 
                # print('==='*40)
                c = re.sub(r'<[^>]+>','',c)  

                # print(c) 
                # print('???'*40)               


                # 删空行
                c = re.sub(r'\s*\n\s*','\n',c)  

                # 将HTML实体转回字符
                import html
                c = html.unescape(c)
                del html    
                
                # print(c) 
                # print('---'*40)
                return_texts.append(c)

        # 按顺序拼回全文
        return_texts = '\n'.join(return_texts)
        
        # 删空行
        return_texts = [return_texts.strip('\n')]
        return return_texts
    

class ZhihuSpider(Spider):
    def __init__(self, database_path, sleep_time=15, mode="external", debug=True):
        super().__init__(database_path, sleep_time, mode, debug)

    def other_rule(self,url):
        # 对要爬取的url做出约束,在该约束下只爬取带有'question'的url的文本;
        # 注意:不带有'question'的url链接仍然会爬取,他们的作用是爬取更多的链接。
        return 'question' in url 
    def pick_webtext(self,html):
        threshold = 50
        important_texts = []
        return_texts = []
        re2 = r'(赞同 \d+)'
        blocks = re.split(re2, html)
        for i,block in enumerate(blocks):
            if block.startswith('赞同'):
                if not important_texts[-1].isdigit():
                    important_texts.append(re.findall(r'\d+',block)[0])
                
                
            elif i+1<len(blocks) and blocks[i+1].startswith('赞同'):
                
                
                
                re1 = r'[\s\S]+[。？！]'
                p = re.findall(re1,block)
                
                
                # 如果有文本中一些英文被删了，尝试调大后面的参数
                reg=r'[\s\da-zA-Z’!"\"#\$%&\(\)\*\+,\-./:;<=>\?@\[\]\^_`\{\|\}~。！，\\\n\t\']{40,}'
                
    #             reg=r'<[^>]+>'
                
                if p:
                    for s in p[-1:]:
                        
                        s = re.sub(reg,'\n',s)
                        
                        s = re.sub(r'</h\d>|</p>','\n',s)
                        
                        s = re.sub(r'<[^>]+>','',s) 
    #                     print(s)
                        important_texts.append(s.split('赞同了该回答')[-1].strip('\n•'))        
        
        for i in range(0,len(important_texts),2):
            if int(important_texts[i+1]) > threshold:
                return_texts.append(important_texts[i])
                
        return return_texts


class RobustSpider(Spider):
    def __init__(self, database_path, sleep_time=15, evaluator=Evaluator(), extractor=Extractor(),mode="external", debug=True, load_old=False):
        super().__init__(database_path, sleep_time, mode, debug, load_old)
        self.evaluator = evaluator
        self.extractor = extractor
    
    def pick_webtext(self,html):
        content = self.extractor.extract_text(html=html)
        content = '\n'.join(content)

        # 删标签
        content = re.sub(r'</h\d>|</p>','\n',content)
        
        content = re.sub(r'\\u003C\\u002Fp\\u003E','\n',content)
        content = re.sub(r'\\u003c\\u002fp\\u003e','\n',content)
        content = re.sub(r'\\u003C\\u002Fh\d\\u003E','\n',content)
        content = re.sub(r'\\u003c\\u002fh\d\\u003e','\n',content)

        content = re.sub(r'\\u003Ch\d\\u003E','\n',content)
        content = re.sub(r'\\u003ch\d\\u003e','\n',content)
        content = re.sub(r'\\u003Cp\\u003E','\n',content)
        content = re.sub(r'\\u003cp\\u003e','\n',content)

        content = re.sub(r'<[^>]+>','',content)
        content = re.sub(r'\\u003C[\s\S]*?\\u003E','',content)
        content = re.sub(r'\\u003c[\s\S]*?\\u003e','',content)
        # print([content])
        # 把unicode转回str
        content = re.sub(r'\\u002F',r'/',content)
        content = re.sub(r'\\u002f',r'/',content)
        content = re.sub(r'\\u003C',r'<',content)
        content = re.sub(r'\\u003c',r'<',content)
        content = re.sub(r'\\u003E',r'>',content)
        content = re.sub(r'\\u003e',r'>',content)
        content = re.sub(r'\\\\n','\n',content)
        content = re.sub(r'\\\\t','\t',content)
        content = re.sub(r'\\\\\\"',r'"',content)
        content = re.sub(r'\\\\',r'\\',content)
        content = re.sub(r'\\n',r'\n',content)
        content = re.sub(r'\\t',r'\t',content)
        
        
        # html实体转回字符
        import html
        content = html.unescape(content)
        del html 

        # 删空行
        content = re.sub(r'\s*\n\s*','\n',content) 

        content = content.lstrip('\n').split('\n')
        return_texts = []
        # 拼回连续文本
        text = ""
        for line in content:
            if not line:
                continue
            if not text:
                text = line 
            else:
                # print("continues:",evaluator.predict(text1=text,text2=line))
                if self.evaluator.is_continuous(text,line):
                    text += line
                # 高赞的概率>0.7
                elif self.evaluator.is_good(text):
                    # 只加入长文本
                    if len(text)>10:
                        return_texts.append(text)
                    text = line
                else:
                    text = line
        if text and self.evaluator.is_good(text):
            return_texts.append(text)
        return return_texts