from flask import Flask
from flask import request
from poliformat import Poliformat
import binascii
import os
import json
p = Poliformat()
app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
      dni = request.form['dni']
      clau = request.form['clau']
      token = binascii.hexlify(os.urandom(16))
      p.login(dni, clau, token)
      ans = {"token":token}
      return json.dumps(ans)
		
@app.route('/sites/<token>/', methods=['GET'])
def sites(token):
	p.load_token(token)
	p.get_sites()
	return json.dumps(p.sites)
	
@app.route('/resources/<token>/<site>/', methods=['GET'])
def resources(token, site):
	p.load_token(token)
	p.get_sites()
	p.get_options(site, 0)
	p.get_resources(site)
	return json.dumps(p.sites[site]["files"])


if __name__ == '__main__':
    app.run()