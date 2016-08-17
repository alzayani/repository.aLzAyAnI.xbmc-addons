# -*- coding: utf8 -*-
try:import sys, syspath
except:pass
import sys
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,os
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from httplib import HTTP
from urlparse import urlparse
import StringIO
import urllib2,urllib
import re
import httplib
import time,itertools

__settings__ = xbmcaddon.Addon(id='plugin.video.movizland')
__icon__ = __settings__.getAddonInfo('icon')
__fanart__ = __settings__.getAddonInfo('fanart')
__language__ = __settings__.getLocalizedString
_thisPlugin = int(sys.argv[1])
_pluginName = (sys.argv[0])
baseurl='http://movizland.com/'
############################################
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_profile_path = xbmc.translatePath(os.path.join(xbmc.translatePath('special://profile'), 'addon_data', addon_id))
if not os.path.exists(addon_profile_path):
    try: xbmcvfs.mkdirs(addon_profile_path)
    except: os.mkdir(addon_profile_path)
	
_cookie_file = xbmc.translatePath(os.path.join(xbmc.translatePath(addon_profile_path), 'cookies.txt'))

cookie_file=_cookie_file
def readnet(url,method='get',form_data={},headers={},html='',proxy='',User_Agent='',cookie_file='',load_cookie=False,save_cookie=False, login=False):
        from addon.common.net import Net
        net=Net()
	if url=='': return ''

	AntiTag='<iframe style="display:none;visibility:hidden;" src="http://my.incapsula.com/public/ga/jsTest.html" id="gaIframe"></iframe>'
	dhtml=''+html
	html=' '+AntiTag+' '
	if not cookie_file: cookie_file = _cookie_file
	if len(User_Agent) > 0: net.set_user_agent(User_Agent)
	else: net.set_user_agent(User_Agent)
	if len(proxy) > 9: net.set_proxy(proxy)
	if (len(cookie_file) > 0) and (load_cookie==True): net.set_cookies(cookie_file)
	xTimes=0
	while (AntiTag in html):
		xTimes=xTimes+1
		if   method.lower()=='get':
			try: html=net.http_GET(url,headers=headers).content
			except urllib2.URLError, e: debob(e); html=dhtml; #debob(url); 
			except Exception, e: debob(e); html=dhtml; #debob(url); 
			except: html=dhtml
		elif method.lower()=='post':
			try: html=net.http_POST(url,form_data=form_data,headers=headers).content #,compression=False
			except urllib2.URLError, e: debob(e); html=dhtml; #debob(url); 
			except Exception, e: debob(e); html=dhtml; #debob(url); 
			except: html=dhtml
		elif method.lower()=='head':
			try: html=net.http_HEAD(url,headers=headers).content
			except urllib2.URLError, e: debob(e); html=dhtml; #debob(url); 
			except Exception, e: debob(e); html=dhtml; #debob(url); 
			except: html=dhtml
		temp_file=xbmc.translatePath(os.path.join(addon_profile_path,'temp.html.--.txt'))
	
		if xTimes > 5: html=html.replace(AntiTag,'')
		elif AntiTag in html: xbmc.sleep(int(addst("AntiTag")))
	if (len(html) > 0) and (len(cookie_file) > 0) and (save_cookie==True): net.save_cookies(cookie_file)
	if "You're browsing too fast! Please slow down." in html: myNote("KissAnime","You're browsing too fast! Please slow down.")
	if "The service is unavailable." in html: deb("HTML","The service is unavailable."); myNote("KissAnime","The service is unavailable.")
        try:html=html.encode("utf-8")
        except:pass
	return html
def debob(e):
        print "error",str(e)
###############################


def readrequest(url):
        r = requests.get(url)
        return r
def read_url2(url):
        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            print 'URL: '+url
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
                #xbmc.executebuiltin("XBMC.Notification(musichcannels,We failed with error code - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: %s' %e.reason
                #xbmc.executebuiltin("XBMC.Notification(LiveStreams,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")
def read_url3(url):#redirect error
        try:


           p = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)

           return p.read()
        except:
                addDir("Download failed:","","",'')
                #xbmc.executebuiltin("XBMC.Notification(LiveStreams,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")                
                return None


def read_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('Host', 'movizland.com')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
	response = urllib2.urlopen(req)
	link=response.read()
	return link

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

def getCategories():
	
	addDir('Search','http://movizland.com/?s=',3,'img/0.png',1)
	addDir('اخــر الاضــافات','http://movizland.com/',15,'img/12.png',1)
	addDir('افلام اجنبية','http://movizland.com/cat/foreign/',11,'img/1.png',1)
	addDir('طلبات الاعضاء','http://movizland.com/tags/?q=submition',16,'img/14.png',1)
	addDir('تجديد روابط الافلام','http://movizland.com/tags/?q=newest',116,'img/16.png',1)
	addDir('بوكس اوفيس','http://movizland.com/tags/?q=boxoffice',106,'img/17.png',1)
	addDir('جودة عالية','http://movizland.com/?type=quality&s=720p+HDTV',126,'img/18.png',1)
	addDir('افلام عربية','http://movizland.com/cat/arab/',11,'img/2.png',1)	
	addDir('افلام هندية','http://movizland.com/cat/india/',11,'img/3.png',1)
	addDir('افلام تركية','http://movizland.com/cat/turkey/',11,'img/8.png',1)
	addDir('افلام اسيوية','http://movizland.com/cat/asia/',11,'img/10.png',1)
	addDir('أفلام مصنفة','url',30,'img/15.png',1)
	addDir('افلام وثائقية','http://movizland.com/cat/documentary/',11,'img/9.png',1)
	addDir('افلام انيميشن','http://movizland.com/cat/anime/',11,'img/4.png',1)
	addDir('مسلسلات اجنبيه','http://movizland.com/cat/foreign-series/',20,'img/6.png',1)
        addDir('مسلسلات عربيه','http://movizland.com/cat/arab-series/',20,'img/5.png',1)
        addDir('مسلسلات تركيه','http://movizland.com/cat/turkey-series/',20,'img/7.png',1)
        
        
        addDir('WWE','url',28,'img/11.png',1)
      
        addDir('برامج تلفزيونية','http://movizland.com/cat/tv-progs/',20,'img/13.png',1)
        
def GENRES(url):
        addDir('••أفلام رعـــب••','http://movizland.com/all/%d8%b1%d8%b9%d8%a8/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/b/b5272b7392e64ef6dcc68fc39578dfd1e4f0b2a6.jpg',1)
        addDir('••الجريمة••','http://movizland.com/all/%d8%ac%d8%b1%d9%8a%d9%85%d9%87/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/a/a7613db07174d97513d2223a5c0e9b991d79fc35.jpg',1)
        addDir('••أفلام رومــــانسية••','http://movizland.com/all/%d8%b1%d9%88%d9%85%d8%a7%d9%86%d8%b3%d9%8a/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/5/5f8e3221b5aaf5d6f314e90e717723fe2fcb50bb.jpg',1)
        addDir('••مغامرات••','http://movizland.com/all/%d9%85%d8%ba%d8%a7%d9%85%d8%b1%d9%87/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/6/62ea53ea057eb4b57b608f7e399787f9dba7c7a3.jpg',1)
        addDir('••كـــومديـــا••','http://movizland.com/all/%d9%83%d9%88%d9%85%d9%8a%d8%af%d9%8a/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/d/d2f385bb5f6644a102a282f8d9413cb386b979b1.jpg',1)
        addDir('••درامــــــــــــا••','http://movizland.com/all/%d8%af%d8%b1%d8%a7%d9%85%d8%a7/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/e/eb0377518bdeaaac851e629fc12923926ef22aff.jpg',1)
        addDir('••الحرب••','http://movizland.com/all/%d8%ad%d8%b1%d8%a8/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/b/b346b21934f4e163523a4fce49038f0a8be9ccd4.jpg',1)
        addDir('••أفلام أكشــــن••','http://movizland.com/all/%d8%a7%d9%83%d8%b4%d9%86/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/4/4ab18ae9829fd44cb6fef620670a87b5db561148.jpg',1)
        addDir('••الخيال العلمي••','http://movizland.com/all/%d8%ae%d9%8a%d8%a7%d9%84-%d8%b9%d9%84%d9%85%d9%8a/',11,'https://cdn.discourse.org/wd/uploads/default/original/2X/b/bc344fd6e8b72734799b00fb83e29e56d78c93c3.jpg',1)
        setView('movies', 'MAIN')
        

	
	
	
        
def WWE(url):
        addDir('WWE','http://movizland.com/cat/other-shows/',20,'img/11.png',1)        
        addDir('WWE-SMAK-DOWN','http://movizland.com/cat/smack-down/',20,'img/11.png',1)      
        addDir('WWE-RAW','http://movizland.com/cat/raw/',20,'img/11.png',1)
        setView('movies', 'MAIN')


        
def search(url):
        
        
         
        search_entered = ''
        debug=True
        if debug:
               keyboard = xbmc.Keyboard(search_entered, 'Search 1channel')
               keyboard.doModal()
               if keyboard.isConfirmed():
                   search_entered = keyboard.getText() .replace(' ','+')  
                   
                   
        else:
             print "search error"
            
        
        
         
        url=url+search_entered
        print "mfarajx4_url",url
          
        getVideos_search("Search",url,1)

def getVideos_search(name1, urlmain,page):
               if page>1:
                  #page-2
                  url_page=urlmain+'/page/'+str(page)+"/"
                  
               else:
                #http://www.dardarkom.com/filme-enline/filme-gharbi/page/2/
                      url_page=urlmain
               print "url_page",url_page
               

               content=readnet(url_page)
               print content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''                                   

               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                        pic = ''
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               if len(match)>15:
                  addDir("next page",urlmain,9,'img/next.png',str(page+1))
def getVideos(name1, urlmain,page):
               if page>1:
                  #page-2
                  url_page=urlmain+'/page/'+str(page)+"/"

                  
                  
               else:
                #http://www.dardarkom.com/filme-enline/filme-gharbi/page/2/
                      url_page=urlmain
               print "url_page",url_page
               _domain_url='www.movizland.com'
               html_=readnet(url_page)
              # print "html",html_
               
               content =html_# readrequest(url_page)
              # print "content1",content
               #content = readrequest(url_page)
               #print "content2",content
               
              # print "fcontent",content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,1,'img/next.png',str(page+1))
def ReqVideos(name1, urlmain,page):
               



               if page>1:
                  #page-2
                
                  url_page='http://movizland.com/tags/page/'+str(page)+'/?q=submition'
                  
                  
                 
                 
               else:
               
                      url_page=urlmain
                      
               print "url_page",url_page
               
               content=readnet(url_page)                
               
               print content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,16,'img/next.png',str(page+1))
               
               
def newestVideos(name1, urlmain,page):
               



               if page>1:
                  
                  url_page='http://movizland.com/tags/page/'+str(page)+'/?q=newest'
                  
                 
                 
               else:
               
                      url_page=urlmain
                      
               print "url_page",url_page
               
               content=readnet(url_page)                
               
               print content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,116,'img/next.png',str(page+1))               
               
def boxoffice(name1, urlmain,page):
               



               if page>0:
                  #page-2
                
                  url_page='http://movizland.com/tags/page/'+str(page)+'/?q=boxoffice'
      
                  
                  
                  
                 
                 
               else:
               
                      url_page=urlmain
                      
               print "url_page",url_page
               
               content=readnet(url_page)                
               
               print content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,106,'img/next.png',str(page+1))
               
def HDTV(name1, urlmain,page):
               



               if page>0:
                  #page-2
                
                  url_page='http://movizland.com/?type=quality&s=720p+HDTV&page='+str(page)+''
                  
                  
                  
                 
                 
               else:
               
                      url_page=urlmain
                      
               print "url_page",url_page
               
               content=readnet(url_page)                
               
               print content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,126,'img/next.png',str(page+1))
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
               
                              
               
def RecentVideos(name1, urlmain,page):
               if page>1:
                  #page-2
                  url_page=urlmain+'/page/'+str(page)+"/"
                  url_page=urlmain+'/?page='+str(page)+"/"
                  #url_page=urlmain+"/"'&page='+str(page)
                  
                  
                  
               else:
                #http://www.dardarkom.com/filme-enline/filme-gharbi/page/2/
                      url_page=urlmain
               print "url_page",url_page
               
               content = readnet(url_page)                
               
               print content
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,15,'img/next.png',str(page+1))
               

def getseries(name1, urlmain,page):
               if page>1:
                  #page-2
                  url_page=urlmain+'/page/'+str(page)+"/"
                  
               else:
                #http://www.dardarkom.com/filme-enline/filme-gharbi/page/2/
                      url_page=urlmain
               print "url_page",url_page
               
               content=readnet(url_page)                 
               
             
               if content is None:
                  addDir('Error:download error','', 1,'',1)
                  return       
               
               #regx='''<div class="moviefilm">\s*<a href="(.*?)">\s*<img .*?src="(.*?)" class="attachment-w-400 wp-post-image" alt="(.*?)"'''
               #regx='''<div class="icon">\s*<a href="(.*?)">\s*<img src="(.*?)" width="180" height="240" title="(.*?)" alt="'''
               regx='''<div class="bottom-title">\s*<a href="(.*?)" title="(.*?)">(.*?)</a>'''
               regx='''<a title="(.*?)" href="(.*?)"><img width="320" height="396" src="(.*?)" class='''
               
               match = re.findall(regx,content, re.M|re.I)
               print "match",match
               
               
               if not match :
                       return
               
               for title,href,image in match:
                       
 
                        url=href
                        
                        try:name=title.encode("utf-8")
                        except:name=title
                        addDir(name,url,2, image)
                        
               
               
               
               addDir("next page",urlmain,20,'img/next.png',str(page+1))               
def getmatch(match):
                if len(match)<1:
                        return
                for href in match:
                    
                    
                    
                    
                     
                    server=href.split("/")[2].replace('www.',"").replace("embed.","").split(".")[0]
                    #if 'hqq' in server or "myvi" in server or 'videomeh' in server:
                            #return
                    addDir(server,href,7,'')


def resolveurl(url):
            from addon.common.net import Net
            net=Net()
            import re,time
            print "url",url
            #sys.exit(0)            

            html=readnet(url)
                              
            id = re.findall('<input type="hidden" name="id" value="(.*?)">',html, re.M|re.I)[0]
            fname = re.findall('<input type="hidden" name="fname" value="(.*?)">',html, re.M|re.I)[0]
            hash = re.findall('<input type="hidden" name="hash" value="(.*?)">',html, re.M|re.I)[0]
            action = re.findall('''<Form method="POST" action='(.*?)'>''',html, re.M|re.I)[0]
            print "id,fname,hash,action",id,fname,hash,action
            time.sleep(5)
            #sys.exit(0)
            data= {
                'imhuman': "Proceed to video",    
                'op': 'download1',
                'usr_login': '',
                'id': id,
                'fname': fname,
                'referer': '',
                'method': 'POST',
                'action': action,
                'hash': hash}   
            result=net.http_POST(url, data, headers={}, compression=True).content
            print "result",result.encode("utf-8")
            return result
def get_servers(url):

	        data=readnet(url)
	        
	        
	        regx='''href="(.+?)">ذهاب الان</a>'''
	        regx='href="(.+?)">.+?</a>'
	        regx='''font-size: 25px;" href="(.+?)">.+?</a>'''
	        match2 = re.findall(regx,data, re.S)
	        print "match2",match2
	        
	        new_url=match2[0]
	        data=resolveurl(new_url)
	        regx='''file:"(.+?)",label:"(.+?)"'''
	       
                match1 = re.findall(regx,data, re.M|re.I)
                print "match1",match1
                for href,title in match1:
                    addDir(title,href,8,'')
                

         
                    
                return            		
def gethosts(urlmain):##cinema and tv featured

                
                data=read_url(urlmain)
                if data is None:
                    return
                
                
                regx1 ='''<iframe.+?src="(.+?)".+?</iframe>'''   
                regx2='''<IFRAME SRC="(.+?)" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=640 HEIGHT=268></IFRAME>'''
                #regx2=''''class="tabcontent"><iframe .+?src="(.+?)".+?></iframe></div>'''
                regx2=''''<iframe .+?src="(.+?)".+?></iframe></div>'''
                
		host1= re.findall(regx1,data, re.M|re.I)
		host2= re.findall(regx2,data, re.M|re.I)
		
		
		if host1:
			 for href in host1:
			   host=gethostname(href)
                           addDir(host,href,2,'')
		if host2:
			 for href in host2:
			   host=gethostname(href)
			   if 'moshahda.net' in href:
                                 mode=21
                           else:
                                 mode=2
                           addDir(host,href,mode,'')                                                

                if not host1 and not host2:                                        
                   addDir("Error:script error or no hoszts found",'',1,'')       
                return
def gethosts2(urlmain):##cinema and tv featured

                
                data=readnet(urlmain)
                print data
                if data is None:
                    return
                regx="'http://moshahda.net/cgi-bin/index_dl.cgi(.*?)'"
		host= re.findall(regx,data, re.M|re.I)
		if host:
                        for href in host:
                          href= 'http://moshahda.net/cgi-bin/index_dl.cgi'+href 
			  playlink(href)

def resolve_host(url):
    if 'vk.com' in url:
            stream_link=resolve_vk(url)
    elif "youwatch" in url:
            stream_link=resolve_youwatch(url)
    elif 'dailymotion' in url:
            print "mfarajx5",url
            
            if not url.startswith('http:'):
                    url='http:'+url
            #url=os.path.split(url)[1]        
            stream_link=resolve_dailymotion(url)
    elif 'youtube' in url:
        videoid = get_youtube_videoid(url)
        stream_link = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % videoid
        listItem = xbmcgui.ListItem(path=str(stream_link))
        xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem)
        return    
    else:        
      import urlresolver
    #hosted_media = urlresolver.HostedMediaFile(url=url, title="host")
      stream_link = urlresolver.resolve(url)
      print "stream_link",stream_link
      if stream_link is None or "unresolvable" in stream_link:
            addDir("Error:unresolvable link","",1,"",1)
            return
    listItem = xbmcgui.ListItem(path=str(stream_link))
    xbmcplugin.setResolvedUrl(_thisPlugin, True, listItem) 
def get_hostlink(url):
	        data=read_url2(url)
                
		
                regx='''<iframe src="(.+?)" width='''
                match = re.findall(regx,data, re.M|re.I)
                print 'match-mfaraj',match,url
                if len(match)<1:
                        regx="'proxy.link'.+?'(.+?)'"
                        match = re.findall(regx,data, re.M|re.I)
                        print 'match-mfaraj2',match,url
                        
                i=0
                for href in match:
                    
     
                    i=i+1
                    server='link1'+str(i)
                    addLink(server,href,7,'')

def resolve_youwatch(url):
		print 'youwatch data'
		from packer import unpack, detect
		data=read_url2(url)
		get_packedjava = re.search("<script type=.text.javascript.>(eval.function.*?)</script>", data, re.S|re.DOTALL)
#		print get_packedjava.group(1)
		if get_packedjava and detect(get_packedjava.group(1)):
			print 'get_packedjava'
			sJavascript = get_packedjava.group(1)
			sUnpacked = unpack(sJavascript)
			if sUnpacked:
				print "unpacked"
#				print sUnpacked
				stream_url = re.search('file:"(.*?)"', sUnpacked, re.S)
				if stream_url:
					link= stream_url.group(1)
					return link
					

		print "no valic stream link found"
                return None    
def resolve_vk(url):
        web_url =url
        print "45m",web_url
        debug=True
        from addon.common.net import Net
        import json as json
        net = Net()
        try:
            soup   = net.http_GET(web_url).content
            html   = soup.decode('cp1251')
            print "html",html
            vars_s = re.findall("""var vars = (.+)""",html)
            if vars_s :
                jsonvars        = json.loads(vars_s[0])
                purged_jsonvars = {}
                for item in jsonvars :
                    if re.search('url[0-9]+', str(item)) :
                        purged_jsonvars[item] = jsonvars[item]               
                lines  = []
                ls_url = []
                for item in purged_jsonvars :
                    ls_url.append(item)
                    quality = item.lstrip('url')
                    lines.append(str(quality))
                if len(ls_url) == 1 :
                    return purged_jsonvars[ls_url[0]].encode('utf-8')
                result =1# xbmcgui.Dialog().select('Choose the link', lines)
                if result != -1 :
                    return purged_jsonvars[ls_url[result]].encode('utf-8')
                else :
                    return None
            else :
                return "No links found"
        except urllib2.URLError, e:
            
            print 'Error','Http error: '+str(e)
            
        except Exception, e:
            print '**** VK Error occured: %s' % e
def playlink(url):
     xbmc.Player().play(url)
     sys.exit(0)
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,mode,iconimage):
    u=_pluginName+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty("IsPlayable","true");
    ok=xbmcplugin.addDirectoryItem(handle=_thisPlugin,url=u,listitem=liz,isFolder=False)
    return ok
	


def addDir(name,url,mode,iconimage,page=1):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



              
params=get_params()
url=None
name=None
mode=None
initial=None
max=None
rating=None
cast=None
year=None
genre=None
duration=None
writer=None
director=None

	
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
	
try:
        mode=int(params["mode"])
except:
        pass
try:
        page=int(params["page"])
except:
        page=1


		


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "page: "+str(page)
if mode==None or url==None or len(url)<1:
        print ""
        getCategories()
       
elif mode==1:
        print ""+url
        getVideos(name,url,page)
elif mode==11:
        print ""+url
        getVideos(name,url,page)
        
elif mode==15:
        print ""+url        
        RecentVideos(name,url,page)
        
elif mode==16:
        print ""+url          
        ReqVideos(name,url,page)
elif mode==116:
        print ""+url        
        newestVideos(name,url,page)
elif mode==106:
        print ""+url         
        boxoffice(name,url,page)
elif mode==126:
        print ""+url         
        HDTV(name,url,page)
elif mode==28:
        print ""+url        
        WWE(url)
         
elif mode==30:
        print ""+url        
        GENRES(url)
elif mode==2:
        print ""+url
        get_servers(url)
elif mode==3:
        print ""+url
        search(url)		

elif mode==6:
        print ""+url
        get_hostlink(url)
elif mode==7:
        resolve_host(url)
elif mode==8:
        playlink(url)
elif mode==9:        
   getVideos_search
elif mode==20:
        getseries(name,url,page)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
