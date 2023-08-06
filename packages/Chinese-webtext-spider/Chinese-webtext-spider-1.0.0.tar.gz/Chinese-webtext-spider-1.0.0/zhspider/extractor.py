import re 
class Extractor:
    def extract_url(self, html: str) :
        pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"')
        urls = pattern.findall(html)
        #print('urls',urls)
        valid_urls = []
        for url in urls:
            if url.startswith('http') or url.startswith('https') or url.startswith('www.') or  url.startswith('//www.'):
                if(url[0:2] == '//'):
                    url='http:'+url
                valid_urls.append(url)
        return valid_urls

    def extract_text(self, html: str):
        #reg=r'[\s\da-zA-Z’!"\"#\$%&\(\)\*\+,\-./:;<=>\?@\]\^_`\{\|\}~。！，\\\n\t\']{10,}'
        reg=r'[\s\da-zA-Z’!\"#\$%&\*\+,\-./:;<=>\?@\]\^_`\{\|\}~。！，`~!@\^\(\)-_=+\|\\\n\t\']{10,}'
        #reg=r'
        # ;:\':,.<>/?'
        p=re.sub(reg,'\n',html)

        # 按换行,制表符给文章分段
        p=re.split(r'\t\n',p)
        valid_docs=[]
        for s in p:
            # 找出所有以[。？！]结尾的字符串
            #print("*"*80)
    
            s = re.findall(r'[\s\d\w《》？：“”+——）（*&……%￥#@！~【】；‘，。’’!"\"#\$%&\(\)\*\+,\-./:;<=>\?@\]\^_`\{\|\}~。！，\\\n\t\']+[。？！]',s)
            
            for c in s:
                valid_docs.append(c)
                   

        return valid_docs

