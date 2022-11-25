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

conn=pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
)

result=""
result2=""
result31=""
result32=""
result33=""
try:
    with conn.cursor() as cursor:
        #Plot 1
        sql="SELECT DATE_FORMAT(dia_hora_inicio, '%Y-%m-%d') as fecha, count(*) as total from evento group by DATE_FORMAT(dia_hora_inicio, '%Y-%m-%d') order by DATE_FORMAT(dia_hora_inicio, '%Y-%m-%d') asc;"
        cursor.execute(sql)
        result=cursor.fetchall()

        #Plot 2
        sql2="SELECT COUNT(*) AS total, tipo FROM evento GROUP BY tipo;"
        cursor.execute(sql2)
        result2=cursor.fetchall()
        

        #Plot 3.1
        sql31="SELECT COUNT(*) as total,DATE_FORMAT(dia_hora_inicio,'%M') as mes FROM evento WHERE TIME('dia_hora_inicio') > '11:00:00' GROUP BY DATE_FORMAT(dia_hora_inicio,'%M');"
        cursor.execute(sql31)
        result31=cursor.fetchall()

        #Plot 3.2
        sql32="SELECT COUNT(*) as total,DATE_FORMAT(dia_hora_inicio,'%M') as mes FROM evento WHERE TIME('dia_hora_inicio')<='11:00:00' and TIME('dia_hora_inicio') >'14:59:00' GROUP BY DATE_FORMAT(dia_hora_inicio,'%M');"
        cursor.execute(sql32)
        result32=cursor.fetchall()

        #Plot 3.3
        sql33="SELECT COUNT(*) as total,DATE_FORMAT(dia_hora_inicio,'%M') as mes FROM evento WHERE TIME('dia_hora_inicio')<='15:00:00' GROUP BY DATE_FORMAT(dia_hora_inicio,'%M');"
        cursor.execute(sql33)
        result33=cursor.fetchall()

finally:
    conn.close()

dictResp1={}
dictResp2={}
dictResp31={}
dictResp32={}
dictResp33={}

if (result!=None):
    i=0
    for x in result:
        dictResp1[str(i)]={}
        dictResp1[str(i)]["fecha"]=x[0]
        dictResp1[str(i)]["total"]=x[1]
        i=i+1

if (result2!=None):
    i=0
    for x in result2:
        dictResp2[str(i)]={}
        dictResp2[str(i)]["total"]=x[0]
        dictResp2[str(i)]["tipo"]=x[1]
        i=i+1

if (result31!=None):
    i=0
    for x in result31:
        dictResp31[str(i)]={}
        dictResp31[str(i)]["total"]=x[0]
        dictResp31[str(i)]["hora"]=x[1]
        i=i+1

if (result32!=None):
    i=0
    for x in result32:
        dictResp32[str(i)]={}
        dictResp32[str(i)]["total"]=x[0]
        dictResp32[str(i)]["hora"]=x[1]
        i=i+1

if (result33!=None):
    i=0
    for x in result33:
        dictResp33[str(i)]={}
        dictResp33[str(i)]["total"]=x[0]
        dictResp33[str(i)]["hora"]=x[1]
        i=i+1

print(dictResp1)
print(dictResp2)
print(dictResp31)
print(dictResp32)
print(dictResp33)