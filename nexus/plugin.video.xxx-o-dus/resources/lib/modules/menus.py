"""
    Copyright (C) 2016 ECHO Coder

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, parse_qsl
from six import PY2
import os,urllib,base64
import kodi
import log_utils

from resources.lib.modules import helper
from resources.lib.modules import utils
from resources.lib.modules import search
from resources.lib.modules import downloader
from resources.lib.modules import parental
from resources.lib.modules import history
from resources.lib.modules import favorites
from resources.lib.modules import picture_viewer
import client
import requests,re,sys
dialog = xbmcgui.Dialog()
translatePath = xbmc.translatePath if PY2 else xbmcvfs.translatePath
#from resources.lib.pyxbmct_.github import xxxgit
from scrapers import __all__
from scrapers import *
messagetext  = 'https://pastebin.com/raw/SgsRvwZV'
AddonTitle   = '[COLOR pink][B]XXX-O-DUS[/B][/COLOR]'
addon_id     = 'plugin.video.xxx-o-dus'
scraper_id   = 'script.xxxodus.scrapers'
artwork_id   = 'script.xxxodus.artwork'
GitUrl       = 'https://raw.githubusercontent.com/nemesis668/repository.streamarmy18-19/main/addons.xml'
buildDirectory = utils.buildDir
specific_icon       = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', '%s/icon.png'))
specific_fanart     = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', '%s/fanart.jpg'))

@utils.url_dispatcher.register('0')


def mainMenu():

    art = translatePath(os.path.join('special://home/addons/script.xxxodus.artwork/resources/art/', 'main/%s.png'))
    popup()
    dirlst = []
    c = []
    c += [
         (kodi.giveColor('Welcome to XXX-O-DUS Version %s' % kodi.get_version() ,'blue',True),translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'icon','Original Code by EchoCoder, Please Report All issues to @Nemzzy668',False), \
         (kodi.giveColor('Official Version Now Maintained By [COLOR yellow]@Nemzzy668[/COLOR]','blue',True),translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'icon','Please Report any issues to @Nemzzy668 On Twitter',False), \
         ('[COLOR yellow]View Changelog[/COLOR]',translatePath(os.path.join(kodi.addonfolder, 'changelog.txt')),17,'changelog','View XXX-O-DUS Changelog.',False), \
         ('[COLOR orange]Check XXX-O-DUS Health',None,46,'icon','Versions',True), \
         ('Search...',None,29,'search','Search XXX-O-DUS',True), \
         ('[COLOR pink]Live Cams',None,37,'webcams','Live Cams',True), \
         ('[COLOR pink]Tubes',None,4,'tubes','Videos',True), \
         #('[COLOR pink]Scenes',None,36,'scenes','XXX Scenes',True), \
         ('[COLOR pink]Movies',None,43,'movies','XXX Movies',True), \
         #('[COLOR pink]Films With Sex In',None,48,'sexfilms','Videos',True), \
         ('[COLOR pink]Virtual Reality',None,42,'vr','XXX Virtual Reality',True), \
         ('[COLOR pink]Hentai',None,39,'hentai','Hentai',True), \
         #('Vintage',None,270,'vintage','Vintage',True), \
         #('[COLOR pink]Fetish',None,40,'fetish','Fetish',True), \
         ('[COLOR pink]Pictures',None,35,'pics','Pictures',True), \
         ('[COLOR pink]For Gay Men',None,47,'gaymen','Videos',True), \
         #('Comics',None,41,'comics','Comics',True), \
         ('[COLOR red]Parental Controls',None,5,'parental_controls','View/Change Parental Control Settings.',True), \
         ('[COLOR red]Your History',None,20,'history','View Your History.',True), \
         ('[COLOR red]Your Favourites',None,23,'favourites','View Your Favourites.',True), \
         ('[COLOR red]Your Downloads',None,27,'downloads','View Your Downloads.',True), \
         ('[COLOR red]Your Settings',None,19,'settings','View/Change Addon Settings.',False), \
         #('View Disclaimer',xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/disclaimer.txt')),17,'disclaimer','View XXX-O-DUS Disclaimer.',False), \
         #('View Addon Information',xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'addon_info','View XXX-O-DUS Information.',False), \
         #('Debug Versions',None,45,'addon_info','View the versions of XXXODUS and its dependencies for debugging.',True), \
         ('RESET XXX-O-DUS',None,18,'reset','Reset XXX-O-DUS to Factory Settings.',False), \
         #(kodi.giveColor('Report Issues @ https://github.com/Colossal1/plugin.video.xxx-o-dus/issues','violet',True),xbmc.translatePath(os.path.join(kodi.addonfolder, 'resources/files/information.txt')),17,'report','All issues must be reported at https://github.com/Colossal1/plugin.video.xxx-o-dus/issues or I will not know the issues exist. I will not provide support at any other location as one central place for everyone to see and discuss issues benefits everyone.',False), \
         ]

    for i in c:
        icon    = art % i[3]
        fanart  = kodi.addonfanart
        dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': i[1], 'mode': i[2], 'icon': icon, 'fanart': fanart, 'description': i[4], 'folder': i[5]})
    #dialog.ok("DIRLIST",str(dirlst))
    buildDirectory(dirlst, cache=False)
    
@utils.url_dispatcher.register('37')


def cams():

    sources = __all__ ; cam_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'cam': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                cam_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if cam_sources:
        dirlst = []
        for i in sorted(cam_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('4')
def tubes():

    sources = __all__ ; video_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".type") == 'video': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                video_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if video_sources:
        dirlst = []
        for i in sorted(video_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)
@utils.url_dispatcher.register('47')
def gaytubes():

    sources = __all__ ; video_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".type") == 'gay': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                video_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if video_sources:
        dirlst = []
        for i in sorted(video_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('48')

def sexfilms():
	sources = __all__ ; video_sources = []; base_name = []; menu_mode = []; art_dir = []
	sources = [i for i in sources if i != 'chaturbate']
	for i in sources:
		try:
			if eval(i + ".type") == 'sexmovies': 
				base_name.append(eval(i + ".base_name"))
				menu_mode.append(eval(i + ".menu_mode"))
				art_dir.append(i)
				video_sources = zip(base_name,menu_mode,art_dir)
		except: pass

	if video_sources:
		dirlst = []
		for i in sorted(video_sources):
			dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

	buildDirectory(dirlst)
@utils.url_dispatcher.register('36')
def scenes():

    sources = __all__ ; scene_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".type") == 'scenes': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                scene_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if scene_sources:
        dirlst = []
        for i in sorted(scene_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('43')
def movies():

    sources = __all__ ; movies_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'movies': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i.replace('_movies',''))
                movies_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if movies_sources:
        dirlst = []
        for i in sorted(movies_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[0].lower(), 'fanart': specific_fanart % i[0].lower(), 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('39')
def hentai():

    sources = __all__ ; hentai_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'hentai': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                hentai_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if hentai_sources:
        dirlst = []
        for i in sorted(hentai_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('41')
def comics():

    sources = __all__ ; comics_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'comics': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".pic_men_mode"))
                art_dir.append(i)
                comics_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if comics_sources:
        dirlst = []
        for i in sorted(comics_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('40')
def fetish():

    sources = __all__ ; fetish_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'fetish': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                fetish_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if fetish_sources:
        dirlst = []
        for i in sorted(fetish_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('42')
def virtualReality():

    sources = __all__ ; vr_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources]
    for i in sources:
        try:
            if eval(i + ".type") == 'vr': 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".menu_mode"))
                art_dir.append(i)
                vr_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if vr_sources:
        dirlst = []
        for i in sorted(vr_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)

@utils.url_dispatcher.register('35')
def pictures():

    sources = __all__ ; picture_sources = []; base_name = []; menu_mode = []; art_dir = []
    sources = [i for i in sources if i != 'chaturbate']
    for i in sources:
        try:
            if eval(i + ".pictures_tag") == 1: 
                base_name.append(eval(i + ".base_name"))
                menu_mode.append(eval(i + ".pic_men_mode"))
                art_dir.append(i)
                picture_sources = zip(base_name,menu_mode,art_dir)
        except: pass

    if picture_sources:
        dirlst = []
        for i in sorted(picture_sources):
            dirlst.append({'name': kodi.giveColor(i[0],'white'), 'url': None, 'mode': i[1], 'icon': specific_icon % i[2], 'fanart': specific_fanart % i[2], 'folder': True})

    buildDirectory(dirlst)
	
@utils.url_dispatcher.register('46')
def versioncheck():
	checkxxx    = translatePath(os.path.join('special://home/addons/' + addon_id, 'addon.xml'))
	checkscraper    = translatePath(os.path.join('special://home/addons/' + scraper_id, 'addon.xml'))
	checkartwork    = translatePath(os.path.join('special://home/addons/' + artwork_id, 'addon.xml'))
	a = open(checkxxx, 'r').read()
	b = re.findall('<addon\s+id=.+?version="(.*?)"',a,flags=re.DOTALL)[0]
	
	c = open(checkscraper, 'r').read()
	d = re.findall('<addon\s+id=.+?version="(.*?)"',c,flags=re.DOTALL)[0]
	
	e = open(checkartwork, 'r').read()
	f = re.findall('<addon\s+id=.+?version="(.*?)"',e,flags=re.DOTALL)[0]
	
	currentversions = requests.get(GitUrl).text
	checkcurrentaddon = re.findall('<addon\s+id="plugin.video.xxx-o-dus".+?version="(.*?)"',currentversions,flags=re.DOTALL)[0]
	checkcurrentscraper = re.findall('<addon\s+id="script.xxxodus.scrapers".+?version="(.*?)"',currentversions,flags=re.DOTALL)[0]
	checkcurrentartwork = re.findall('<addon\s+id="script.xxxodus.artwork".+?version="(.*?)"',currentversions,flags=re.DOTALL)[0]
	
	messagestring = ''
	if b == checkcurrentaddon:
		string = ('[COLOR lime]XXX-O-DUS Current : %s | Your Version : %s | All Up To Date[/COLOR]\n' % (checkcurrentaddon,b))
	elif b < checkcurrentaddon:
		string = ('[COLOR orange]XXX-O-DUS Current : %s | Your Version : %s | Addon Out Of Date[/COLOR]\n' % (checkcurrentaddon,b))
	elif b > checkcurrentaddon:
		string = ('[COLOR red][B]XXX-O-DUS Current : %s | Your Version : %s | Malicous Version Detected - Recommended You Un-install[/B][/COLOR]\n' % (checkcurrentaddon,b))
	
	if d == checkcurrentscraper:
		string = string + ('[COLOR lime]Scraper MODULE Current : %s | Your Version : %s | All Up To Date[/COLOR]\n' % (checkcurrentscraper,d))
	elif d < checkcurrentscraper:
		string = string + ('[COLOR orange]Scraper MODULE : %s | Your Version : %s | Module Out Of Date[/COLOR]\n' % (checkcurrentscraper,d))
	elif d > checkcurrentscraper:
		string = string + ('[COLOR red][B]Scraper MODULE : %s | Your Version : %s | Malicous Version Detected - Recommended You Un-install[/B][/COLOR]\n' % (checkcurrentscraper,d))
		
	if f == checkcurrentartwork:
		string = string + ('[COLOR lime]Artwork MODULE Current : %s | Your Version : %s | All Up To Date[/COLOR]\n' % (checkcurrentartwork,f))
	elif f < checkcurrentartwork:
		string = string + ('[COLOR orange]Artwork MODULE : %s | Your Version : %s | Module Out Of Date[/COLOR]\n' % (checkcurrentartwork,f))
	elif f > checkcurrentartwork:
		string = string + ('[COLOR red][B]Artwork MODULE : %s | Your Version : %s | Malicous Version Detected - Recommended You Un-install[/B][/COLOR]\n' % (checkcurrentartwork,f))
		
	showText(AddonTitle,string)

def popup():
    pass
    # try:
        # message = requests.get(messagetext).text
        # if len(message)>1:
            # path = xbmcaddon.Addon().getAddonInfo('path')
            # comparefile = os.path.join(os.path.join(path,''), 'popup.txt')
            # r = open(comparefile)
            # compfile = r.read()
            # if str(len(compfile)) == str(len(message)): pass
            # else:
                # showText('[B][COLOR pink]XXX-O-DUS LATEST NEWS[/B][/COLOR]', message)
                # text_file = open(comparefile, "w")
                # text_file.write(message)
                # text_file.close()
    # except: pass

def showText(heading, text):

	try:
		id = 10147
		xbmc.executebuiltin('ActivateWindow(%d)' % id)
		xbmc.sleep(500)
		win = xbmcgui.Window(id)
		retry = 50
		while (retry > 0):
			try:
				xbmc.sleep(10)
				retry -= 1
				win.getControl(1).setLabel(heading)
				win.getControl(5).setText(text)
				quit()
				return
			except: pass
	except: pass

