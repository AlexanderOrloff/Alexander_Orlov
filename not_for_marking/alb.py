import urllib.request
import re

pageURL = 'http://www.forumishqiptar.com/threads/162493-Announcement-Post-New-4'
def download_page(pageURL ):
    
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
    
    return links
def cleaning (links):
    texts = []
    for link in links: 
        with urllib.request.urlopen(link) as response:
           html = response.read().decode('ISO-8859-1')
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)  # это рег. выражение находит все тэги
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) # все скрипты
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)  # все комментарии

    
        clean_t = regScript.sub("", html)
        clean_t = regComment.sub("", clean_t)
        clean_t = regTag.sub("", clean_t)
        texts.append(clean_t)
    print (texts[1])
cleaning(download_page(pageURL ))

			
