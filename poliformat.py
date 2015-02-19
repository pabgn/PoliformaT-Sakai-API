import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import os

class Poliformat:
	
	def __init__(self):
		self.cookie = "cookie.txt"
		self.cj = cookielib.LWPCookieJar()
		self.br = mechanize.Browser()
		self.br.set_cookiejar(self.cj)
		self.br.set_handle_equiv(True)
		self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		self.br.addheaders = [('User-agent', 'Chrome')]
		self.sites={}
		#if os.path.isfile(self.cookie):
			#self.cj.load(self.cookie, ignore_discard=True, ignore_expires=True)
	
	def load_token(self, token):
		if os.path.isfile("cookies/"+token+".txt"):
			self.cj.load("cookies/"+token+".txt", ignore_discard=True, ignore_expires=True)
	
	def login(self, dni, clau, token):

		n = self.br.open('https://www.upv.es/pls/soalu/est_intranet.NI_Indiv?P_IDIOMA=c&P_MODO=alumno&P_CUA=sakai&P_VISTA=MSE')
		self.br.select_form(nr=0)
		self.br.form['dni'] = dni
		self.br.form['clau'] = clau
		self.br.submit()
		self.br.open('https://poliformat.upv.es/portal')
		self.get_sites()
		self.cj.save("cookies/"+token+".txt", ignore_discard=True, ignore_expires=True)


	def get_sites(self):
		b = BeautifulSoup(self.br.open('https://poliformat.upv.es/portal/tool/86ac4519-944d-49e5-a701-b03843f93614?panel=Main').read())
		ops = b.find('select', {'name':'prefs_form:_id36'})
		actives = ops.findChildren()
		for c in actives:
			self.sites[c.contents[0]]={"id":c['value'], "options":{}}
		ops = b.find('select', {'name':'prefs_form:_id44'})
		inactives = ops.findChildren()		
		for c in inactives:
			self.sites[c.contents[0]]={"id":c['value'], "options":{}}

	def get_options(self, key, t):
		b = BeautifulSoup(self.br.open('https://poliformat.upv.es/portal/site/'+self.sites[key]["id"]).read())
		ops = b.find('div', {'id':'toolMenu'}).findChildren()[0]
		last = ""
		for li in ops.findAll('li'):
			if li.findChildren()[0].has_key('href'):
				self.sites[key]["options"][li.findChildren()[0].findChildren()[0].contents[0]]= li.findChildren()[0]["href"]
				last = li.findChildren()[0].findChildren()[0].contents[0]
		if t==0:
			self.get_panel(key, last)
			self.get_options(key, 1)
		self.sites[key]["options"]["Recursos"]='https://poliformat.upv.es/access/content/group/'+self.sites[key]["id"]+"/"
	def get_panel(self, key, item):
		b = BeautifulSoup(self.br.open(self.sites[key]["options"][item]).read())	
		i = b.find('iframe')
		self.sites[key]["options"][item]=i["src"]
	
	def get_resources(self, key):
		self.sites[key]["files"]=[]
		b = BeautifulSoup(self.br.open(self.sites[key]["options"]["Recursos"]).read())	
		rows =  b.findAll("li",{"class":"folder"})
		for r in rows:
			self.sites[key]["files"].append({"name":r.find("a").contents[0], "link":r.find("a")['href']})

	def print_resources(self, key):
		
		for f in self.sites[key]["files"]:
			print f["name"]
	
	def go_level(self, key, n):
		
		self.sites[key]["options"]["Recursos"]+=self.sites[key]["files"][n]["link"]
	
