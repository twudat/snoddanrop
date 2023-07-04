from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl, urljoin
from six import PY2

import os,re
import kodi
import client
import cache
import dom_parser2
import log_utils
from resources.lib.modules import utils
buildDirectory = utils.buildDir
dialog = xbmcgui.Dialog()
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
class scraper:

    def get_list(self, mode, type, url, title_pattern, url_pattern, icon_pattern=None, site=None, d_p1=None, d_p2=None, d_p3=None, parse=None, cache_time=None,searched=False,stopend=False, isVideo=False, isDownloadable = False):

        if cache_time: r = cache.get(client.request,cache_time,url)
        else: r = client.request(url)

        if 're|' in d_p3:
            d_p3 = d_p3.replace('re|','')
            r = dom_parser2.parse_dom(r, d_p1, {d_p2: re.compile('%s' % d_p3)})
        else: r = dom_parser2.parse_dom(r, d_p1, {d_p2: d_p3})

        if r:
        
            dirlst = []
            
            for i in r:
                    name = re.findall(r'%s' % title_pattern,i.content)[0]
                    name = kodi.sortX(i[1].encode('utf-8'))
                    url = re.findall(r'%s' % url_pattern,i.content)[0]
                    if icon_pattern:
                        iconimage = re.findall(r'%s' % icon_pattern,i.content)[0]
                    elif site: iconimage = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % site))
                    else: iconimage = translatePath(os.path.join('special://home/addons/' + kodi.get_id(), 'icon.png'))
                    fanarts = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % site))
                    if parse: 
                        link,tag = parse.split('|SPLIT|')
                        if tag == 'url': 
                            url = urlparse.urljoin(link,url)
                        elif tag == 'icon': 
                            iconimage = urlparse.urljoin(link,iconimage)
                        else:
                            url = urlparse.urljoin(link,url)
                            iconimage = urlparse.urljoin(link,iconimage)
                    if site: url += '|SPLIT|' + site        
                    if type == 'dir': dirlst.append({'name': kodi.giveColor(name,'white'), 'url': url, 'mode': mode, 'icon': iconimage, 'fanart': fanarts, 'description': name, 'folder': True})
                    else: dirlst.append({'name': kodi.giveColor(name,'white'), 'url': url, 'mode': mode, 'icon': iconimage, 'fanart': fanarts, 'description': name, 'folder': False})

            if dirlst: 
                if stopend: buildDirectory(dirlst, stopend=True, isVideo=isVideo, isDownloadable=isDownloadable)
                else: buildDirectory(dirlst, isVideo=isVideo, isDownloadable=isDownloadable)

    def get_next_page(self, mode, url, pattern, site='', parse=None, pictures=False):
        try:
            dirlst = []
            icon = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/main/next.png'))
            fanart = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % site))
            if '|GOT_URL' in url: 
                url = url.split('|GOT_URL')[0]
                dirlst.append({'name': kodi.giveColor('Next Page -->','white'), 'url': url, 'mode': mode, 'icon': icon, 'fanart': fanart, 'description': 'Load More......', 'folder': True})
            else: 
                r = client.request(url)
                url2 = re.findall(r'%s' % pattern,r)[0]
                if parse:
                    url2 = urljoin(parse,url2)
                elif '&amp;' in url2: url2 = url2.replace('&amp;','&')
                elif 'mydirtyhobby' in url:
                    url2 = 'https://www.mydirtyhobby.com'+url2
                dirlst.append({'name': kodi.giveColor('Next Page -->','white'), 'url': url2, 'mode': mode, 'icon': icon, 'fanart': fanart, 'description': 'Load More......', 'folder': True})
            if 'chaturbate' in url:
                if dirlst: buildDirectory(dirlst, isVideo=True, chaturbate=True)
            elif pictures:
                if dirlst: buildDirectory(dirlst, pictures=True)
            else:
                if dirlst: buildDirectory(dirlst, isVideo=True)
        except Exception as e:
            log_utils.log('Error getting next page for %s :: Error: %s' % (site.title(),str(e)), log_utils.LOGERROR)
            xbmcplugin.setContent(kodi.syshandle, 'movies')
            if 'chaturbate' in url: utils.setView('chaturbate')
            elif pictures: utils.setView('pictures')
            else: utils.setView('thumbs')
            xbmcplugin.endOfDirectory(kodi.syshandle, cacheToDisc=True)