# -*- coding: utf-8 -*-

from flask import Flask
from flask import escape, request, Response, url_for, render_template, flash, redirect, jsonify
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask.ext import uploads
from flask.ext.uploads import IMAGES, configure_uploads, patch_request_class
import flask

import urllib2, urllib, json, simplejson
import xml.dom.minidom as minidom
import htmllib

from random import choice

app = Flask(__name__)

###
# Hardcoded web site variables, uncomment to get this working on the test server
#htmlpage = 'X'
#pythonpage = 'X'

#Local web site variables, uncomment to get this working when running locally
htmlpage = '/'
pythonpage =''

css = htmlpage + 'static/wememe.css'
###


#GNU Affero Public License Statement
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
    
#function to acquire the json for a web page at x. Useful for searching Twitter.
def jsonjson(x):
     req = urllib2.Request(x)
     opener = urllib2.build_opener()
     instance = opener.open(req)
     return simplejson.load(instance)

#code modified from http://www.blog.pythonlibrary.org/2010/11/12/python-parsing-xml-with-minidom/
def pullrandimage(feed):
    """
    Pulls all image links found in Tumblr xml and selects one at random.
    """
    newfeed = minidom.parse(urllib.urlopen(feed))
    newnewfeed = []
    linkfeed = []
    newnewfeed = newfeed.getElementsByTagName('photo-url')
    for feed in newnewfeed:
        nodes = feed.childNodes
        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                linkfeed.append(node.data)
    return choice(linkfeed)

#Enter Twitter feed and Tumblr URL here
tumblraccount1 = 'http://wememechina.tumblr.com'
tumblraccount2 = 'http://wememeamerica.tumblr.com'


@app.route('/index')
def wememelandingpage():
    try:
        #Return template
        img1 = pullrandimage(tumblraccount1 + '/api/read?&num=10')
        img2 = pullrandimage(tumblraccount2 + '/api/read?&num=10')
        return render_template('wememe.html',css=css,img1=img1,img2=img2,htmlpage=htmlpage,pythonpage=pythonpage)
    except:
        print "oops"
        
@app.route('/statement')
def statementpage():
    try:
        #Return template
        return render_template('statement.html',css=css,htmlpage=htmlpage)
    except:
        print "oops"
        
@app.route('/technical')
def technicalpage():
    try:
        #Return template
        return render_template('technical.html',css=css,htmlpage=htmlpage)
    except:
        print "oops"
        
@app.route('/img1only')
def firstscreen():
    try:
        #Return template
        img = pullrandimage(tumblraccount1 + '/api/read?&num=10')
        title=u'中国'
        return render_template('wememesingleimage.html',css=css,img=img)
    except:
        print "oops"

@app.route('/img2only')
def secondscreen():
    try:
        img = pullrandimage(tumblraccount2 + '/api/read?&num=10')
        title="America"
        #Return template
        return render_template('wememesingleimage.html',css=css,img=img)
    except:
        print "oops"

if __name__ == '__main__':
    app.run(debug=True)
