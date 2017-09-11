import urllib.request
import re
def opening():
    url = 'http://istoki-rb.ru/' 
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request ('http://istoki-rb.ru/', headers = {'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
    return html
def titeling(html):
    titles = []
    comtitles = re.compile ("<div class='title'>(.*?)</div>", flags = re.DOTALL)
    titles = comtitles.findall(html)
    new_titles = []
    regTag = re.compile('<.*?>', flags =re.DOTALL)
    regSpace = re.compile('\s{2,}', flags = re.DOTALL)
    for t in titles:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t)
        new_titles.append(clean_t)
    return new_titles
def writing(new_titles):
    f = open ('text.txt', 'w', encoding = 'utf-8')
    for t in new_titles:
        twrite = t + '\n'
        f.write(twrite)
    f.close()
writing(titeling(opening()))
