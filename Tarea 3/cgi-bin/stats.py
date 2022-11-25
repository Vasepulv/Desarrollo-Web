#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import cgi
import cgitb
import pymysql
import json
from pymysql.cursors import Cursor

cgitb.enable()

print("Content-type: text/html; charset=UTF-8") # <-- Esto dice al interprete que es una pagina web
print("")
print("<html><head><link href='/~vasepulv/style.css' rel='stylesheet' type='text/css'></head>")
print("<body>")
print("<div id='plot1'></div>")
print("<div id='plot2'></div>")
print("<div id='plot31'></div>")
print("<div id='plot32'></div>")
print("<div id='plot33'></div>")
print("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script>")
print("<script src='https://code.highcharts.com/highcharts.src.js'></script>")
print("<script src='/~vasepulv/statsScript.js'></script>")