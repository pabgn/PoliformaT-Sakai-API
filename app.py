#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from poliformat import Poliformat
import binascii
import os
import json
from urllib import quote

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
      data = request.get_json()
      dni = data['dni']
      clau = data['clau']
      token = binascii.hexlify(os.urandom(16))
      p = Poliformat()
      try:
      	p.login(dni, clau, token)
        ans = {"token":token}
      except:
        ans = {"error":"DNI or Clau incorrect"}
      
      return json.dumps(ans)
		
@app.route('/sites/<token>/', methods=['GET'])
def sites(token):
	p = Poliformat()
	p.load_token(token)
	p.get_sites()
	return json.dumps(p.sites)
	
@app.route('/resources/<token>/<site>', methods=['GET'])
def resources(token, site):
	path = request.args.get('path', '')
	p = Poliformat()
	p.load_token(token)
	p.get_sites()
	p.get_options(site, 0)
	if(len(path)>0):
		p.sites[site]["files"]["navigation"]["current"]+=quote(path.encode('utf8'))
	p.get_resources(site)
	return json.dumps(p.sites[site]["files"]["tree"])


if __name__ == '__main__':
    app.run()