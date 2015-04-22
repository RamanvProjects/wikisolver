import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('http://en.wikipedia.org/wiki/Chemistry')

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        print link['href']
