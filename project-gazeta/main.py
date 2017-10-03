import urllib.request
import re
import os
import time

#программа начинает работу в  заранее созданной папке gazeta на рабочем столе, в которой также лежит mystem, папки plain, mystem-xml и mystem-txt
#так как у данной газеты есть архив  новостей, где можно с первой страницы архива сразу перейти на последнюю, число страниц разумнее узнать вручную 

def page_urls():
     main_url = 'http://www.selpravda.ru/news.html?page='
     urls = []
     for i in range(1,703):
         page_url = main_url + str(i)
         time.sleep(2)
         page = urllib.request.urlopen(page_url)
         text = page.read().decode('windows-1251')
         regLink =re.compile('class="mnname"><a href="(.*?)">.*?</a></div>')
         links = regLink.findall(text)
         for link in links:
             url = 'http://www.selpravda.ru' + link
             urls.append(url)
     return urls

def texts(urls):
    i = 0
    for url in urls:
       page = urllib.request.urlopen(url)
       time.sleep(2)
       text = page.read().decode('windows-1251')
       topic = re.search('<h1>(.*?)</h1>', text)
       topic1 = topic.group(1)
       date = re.search('<div class="mndata">(.*?)</div>', text)
       date1 = date.group(1)
       title = re.search('<h2>(.*?)</h2>', text )
       title1 = title.group(1)
       article = cleaner(text)
       #if article.endswith('.') == False and article.endswith('!') ==False and article.endswith('?') == False:
            #author1 = article.split()[-2:]
       #else:
            #author1 = 'Noname'
       #к сожалению, в некоторых случаях посде имени автора ставилась точка, и, наоборот, не ставилось точки после фразы "авторские фото" в конце статьи, в связи с чем одназночно извлечь имена авторов не представляется возможным
       i +=1
       writing(url, topic1, date1, title1, article, i)
       
def cleaner(text):
     article = re.search('</h2>(.*)"comment">', text, re.DOTALL)
     regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
     regSpace = re.compile('\s{2,}', re.DOTALL)
     clean_t = regTag.sub("", article.group(0))
     clean_t = regSpace.sub('', clean_t)
     clean_t = re.sub('&laquo;','«', clean_t)
     clean_t = re.sub('&raquo;','»', clean_t)
     clean_t = re.sub('&bull;','•', clean_t)
     clean_t = re.sub('&frasl;','⁄', clean_t)
     clean_t = re.sub('&quot;','"', clean_t)
     clean_t = re.sub('&nbsp;',' ', clean_t)
     clean_t = re.sub('&ndash;',' - ', clean_t)
     clean_t = re.sub('&hellip;','...', clean_t)
     clean_t = re.sub('&ldquo;','“', clean_t)
     clean_t = re.sub('&rdquo;','”', clean_t)
     clean_t = re.sub('&mdash;','—', clean_t)
     clean_t = re.sub('&mdash;','—', clean_t)
     return clean_t

def writing(url, topic1, date1, title1, article, i):
    m = re.search('\d\d.(\d\d).(\d\d\d\d)', date1)
    subdir = os.path.join(str(m[2]), str(m[1]))
    directory = os.path.join('plain', subdir)
    if os.path.exists(directory) == False:
        os.makedirs(directory)
    filename =  str(i) + '.txt'                         
    filepath = os.path.join(directory, filename)
    with open(filepath, 'a', encoding = 'utf-8') as f:
          au = '@au Noname' + '\n'
          f.write(au)
          ti = '@ti ' + title1 + '\n'
          f.write(ti )
          da = '@da ' + date1 + '\n'
          f.write(da)
          topic = '@topic ' + topic1 + '\n'
          f.write(topic)
          URL ='@url ' + url + '\n'
          f.write(article)
    mystem( subdir, 'xml', i, filepath)
    mystem( subdir, 'txt', i, filepath)
    meta (filepath, title1, date1, topic1, url ,  str(m[2]) )
         
def mystem(subdir, form, i, filepath):
     if  form == "xml":
          dirname = 'mystem-xml'
     else:
          dirname = 'mystem-txt'
     myfilename =  str(i) +'.'+ form
     mydirectory = os.path.join(dirname,subdir )
     if os.path.exists(mydirectory) == False:
        os.makedirs(mydirectory)
     myfilepath = os.path.join(mydirectory, myfilename)
     if form == 'xml':
          os.system (r'.\mystem.exe'+ ' '+'-nid --format '+ form + ' ' + filepath + ' ' + myfilepath)
     else:
          os.system (r'.\mystem.exe'+ ' '+'-nid ' + ' ' + filepath + ' ' + myfilepath)

def meta(filepath, title1, date1, topic1, url , year):
     with open (r'C:\Users\Александр Орлов\Desktop\gazeta\metadata.csv', 'a', encoding ='utf-8') as g:
          row = '%s\t%s\t\t\tNoname\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tCельская_правда\t\t%s\tгазета\tРоссия\tМокшан-ПензенскаяОбласть\tru'
          g.write(row % (filepath, title1, date1, topic1, url , year))
          g.write('\n')
          
#if '__name__' == '__main__'
texts(page_urls())
