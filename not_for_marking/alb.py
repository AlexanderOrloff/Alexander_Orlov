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
        print (pageURL)
        
    
    return links
print (download_page(pageURL ))

			
