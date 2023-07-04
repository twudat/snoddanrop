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
dialog = xbmcgui.Dialog()
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'http://www.motherless.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 210
content_mode = 211
player_mode  = 801

search_tag   = 1
search_base  = urljoin(base_domain,'term/%s')

pictures_tag = 1
pic_men_mode = 260
pic_con_mode = 261
pic_v_mode   = 805

"""""""""
        The section below is dedicated to the video aspect of the scraper 
"""""""""

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():

	lover.checkupdates()

	try:
		url = base_domain
		c = client.request(url)
		soup = BeautifulSoup(c,'html.parser')
		data = soup.find('div', class_={'menu-categories-tabs-container'})
		if ( not data ):
			log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
			kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
			quit()
	except Exception as e:
		log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
		kodi.notify(msg='Fatal Error', duration=4000, sound=True)
		quit()
		
	dirlst = []

	for i in data.find_all('a'):
		try:
			name = i.text
			url2 = i['href']+'/videos'
			if not base_domain in url2: url2=base_domain+url2
			icon = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
			fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
			dirlst.append({'name': name, 'url': url2, 'mode': content_mode, 'icon': icon, 'fanart': fanarts, 'folder': True})
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
        soup = BeautifulSoup(c,'html.parser')
        r = soup.find_all('div', class_={'thumb-container video'})
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
            name = i.find('img', class_={'static'})['alt'].title()
            url2 = i.a['href']
            icon = i.find('img', class_={'static'})['src']
            icon = icon+'|verifypeer=false'
            fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': url2, 'mode': player_mode, 'icon': icon, 'fanart': fanarts,'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)

    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))

    if not searched:
        search_pattern = '''a\s*href=['"]([^'"]+)['"]\s*class=['"]pop['"]\s*rel=['"]\d+['"]>NEXT'''
        parse = base_domain
        
        helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)
        
"""""""""
        The section below is dedicated to the picture aspect of the scraper 
"""""""""

@utils.url_dispatcher.register('%s' % pic_men_mode)
def pic_menu():
    
    try:
        url = urljoin(base_domain,'images')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'h1')
        r = [(dom_parser2.parse_dom(i, 'a', req='href')) for i in r if i]
        r = [(urljoin(base_domain,i[0].attrs['href']),i[0].content) for i in r if i]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []
    
    for i in r[:-1]:
        try:
            if PY2: name = kodi.sortX(i[1].encode('utf-8')).title()
            else: name = kodi.sortX(i[1]).title()
            icon = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
            fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': pic_con_mode, 'icon': icon, 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst)    
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()
        
@utils.url_dispatcher.register('%s' % pic_con_mode, ['url'])
def pic_content(url):
    
    try:
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div', {'class': 'thumb-container'})
        r = [(dom_parser2.parse_dom(i, 'a', req='href'), \
              dom_parser2.parse_dom(i, 'img', req=['src','alt'])) \
              for i in r if i]
        r = [(i[0][0].attrs['href'], i[1][0].attrs['alt'], i[1][0].attrs['src']) for i in r if i[0]]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []
    
    for i in r:
        try:
            if PY2: name = kodi.sortX(i[1].encode('utf-8')).title()
            else: name = kodi.sortX(i[1]).title()
            fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': pic_v_mode, 'icon': i[2], 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: 
        buildDirectory(dirlst, stopend=True, pictures=True)    
        search_pattern = '''<a\s*href=['"]([^'"]+)['"]\s*class=['"]pop['"]\s*rel=['"]\d+['"]>NEXT'''
        parse = base_domain
        helper.scraper().get_next_page(pic_con_mode,url,search_pattern,filename,parse,pictures=True)
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()        