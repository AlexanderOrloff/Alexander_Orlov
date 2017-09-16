import urllib.request
import re

pageURL = 'http://www.forumishqiptar.com/threads/162493-Announcement-Post-New-4'
def download_page(pageURL ):
    texts = []
    links = []
    while True:
        links.append(pageURL)
     
        req = urllib.request.Request(pageURL)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('ISO-8859-1')
        link = re.search('<!-- next / previous links --(.*?)<a href="(.*?)">', html, re.DOTALL )
        pageURL= 'http://www.forumishqiptar.com/' + link.group(2)

        if pageURL in links:
            break
        texts.append(cleaning(html))
    return texts
def cleaning(html):
        words = re.findall('<div class="content">.*?</div>', html, re.DOTALL)
        
    
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)  # это рег. выражение находит все тэги
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) # все скрипты
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)  # все комментарии
        regSpace = re.compile('\s{2,}', re.DOTALL)

        for word in words:
            clean_t = regScript.sub("", word)
            clean_t = regComment.sub("", clean_t)
            clean_t = regTag.sub("", clean_t)
            clean_t = regSpace.sub("", clean_t)
            print(clean_t)
            
        return clean_t

download_page(pageURL )

