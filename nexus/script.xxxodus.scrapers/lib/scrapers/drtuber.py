from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl, urljoin
from six import PY2
from resources.lib.modules import lover
from resources.lib.modules import utils
from resources.lib.modules import helper
import log_utils
import kodi
import client
import dom_parser2, os,re
from bs4 import BeautifulSoup
buildDirectory = utils.buildDir #CODE BY NEMZZY AND ECHO
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'http://www.drtuber.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 258
content_mode = 259
player_mode  = 801

search_tag   = 1
search_base  = urljoin(base_domain,'search/videos/%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
	lover.checkupdates()

	try:
		url = urljoin(base_domain, 'categories')
		c = client.request(url)
		soup = BeautifulSoup(c, 'html5lib')
		content = soup.find('div', class_={'ID-list-category'})
		if ( not content ):
			log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
			kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
			quit()
	except Exception as e:
		log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
		kodi.notify(msg='Fatal Error', duration=4000, sound=True)
		quit()

	dirlst = []

	for a in content.find_all('a'):
		try:
			title = a.span.text.title()
			url = a['href']
			if not base_domain in url: url = base_domain+url
			icon = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
			fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
			dirlst.append({'name': title, 'url': url, 'mode': content_mode, 'icon': icon, 'fanart': fanarts, 'folder': True})
		except Exception as e:
			log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)

	if dirlst: buildDirectory(dirlst)    
	else:
		kodi.notify(msg='No Menu Items Found')
		quit()

@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

    try:
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'a')
        r = [i for i in r if '<em class="time_thumb">' in i.content]
        r = [(i.attrs['href'], \
              dom_parser2.parse_dom(i.content, 'img', req=['src','alt']), \
              dom_parser2.parse_dom(i.content, 'em', {'class': 'time_thumb'})) \
            for i in r]
        r = [(urljoin(base_domain,i[0]), i[1][0].attrs['alt'], re.sub('<.+?>', '', i[2][0].content), i[1][0].attrs['src']) for i in r]
        if ( not r ) and ( not searched ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
    except Exception as e:
        if ( not searched ):
            log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
            kodi.notify(msg='Fatal Error', duration=4000, sound=True)
            quit()    
        else: pass
    
    dirlst = []
        
    for i in r:
        try:
            if PY2: name = '%s - [ %s ]' % (kodi.sortX(i[1].encode('utf-8')).title(),kodi.sortX(i[2].encode('utf-8')))
            else:name = '%s - [ %s ]' % (kodi.sortX(i[1]).title(),kodi.sortX(i[2]))
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[3], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))
    
    if not searched:
        
        try:
            search_pattern = '''<li\s*class=['"]next['"]><a\s*href=['"]([^'"]+)'''
            parse = base_domain        
            helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)
        except Exception as e: 
            log_utils.log('Error getting next page for %s :: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)