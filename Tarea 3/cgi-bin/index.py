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
print("<html><head><link href='/~vasepulv/style.css' rel='stylesheet' type='text/css'>")
print("""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
   integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
   crossorigin=""/>
""")

print("""
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
   integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
   crossorigin=""></script>
""")

print("</head>")
# El body del HTML
body=f"""<body>
<table>
            <tr>
                <td><a href="/~vasepulv/cgi-bin/form.py"><button type="button">Informar Evento</button></a></td>
                <td><a href="/~vasepulv/cgi-bin/list.py"><button type="button">Ver listado de Eventos</button></a></td>
                <td><a href="/~vasepulv/cgi-bin/stats.py"><button type="button">Estadísticas</button></a></td>
            </tr>
 </table>
"""
print(body)

print("""
    <h1>Bienvenidos</h1>
    "<div id='map' style="width: 600px; height: 400px;">
""")
print("<script src='/~vasepulv/mapScript.js'></script>")

conn= pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
)

try:
    result=""
    result2=""
    result3=""
    f=open('../chile.json')
    dictComuna=json.load(f)
    x=[]
    with conn.cursor() as cursor:
        sql="SELECT id,comuna_id FROM evento;"
        cursor.execute(sql)
        result=cursor.fetchall()

        for id, comuna_id in result:
            sql2="SELECT count(*) FROM foto WHERE evento_id=(%s);"
            cursor.execute(sql2,id)
            result2=cursor.fetchall()

            sql3="SELECT nombre FROM comuna WHERE id=(%s);"
            cursor.execute(sql3,comuna_id)
            result3=cursor.fetchone()

            v=[x for x in dictComuna if x["name"]==result3[0]]
            x.append(v[0])

        
finally:
    conn.close()

for i in x:
    print("<script type='text/javascript' language='JavaScript'>addMarker("+i["lng"]+","+i["lat"]+","+"'"+i["name"]+"'"+");</script>")

print("</div>")

print("""
        <div>Ultimos 5 eventos informados</div>
""")


table="""
<table>
    <tr>
                <td>Fecha - Hora de Inicio:</td>
                <td>Fecha - Hora de Termino:</td>
                <td>Comuna</td>
                <td>Sector</td>
                <td>Tipo</td>
                <td>Foto</td>
    </tr>
"""
print(table)

conn= pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
)
result=""
try:
    with conn.cursor() as cursor:
        sql="SELECT id, comuna_id, sector, dia_hora_inicio, dia_hora_termino,tipo FROM evento ORDER BY id DESC LIMIT 5;"
        cursor.execute(sql)
        result=cursor.fetchall()

finally:
    conn.close()

if (len(result)==0):
    value="""
    <tr>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
            </tr>
    """
    print(value)


    
else:
    conn= pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
    )
    for id,comuna,sector,dia_inicio,dia_termino,tipo in result:
        resultado=""
        result2=""
        try:
            with conn.cursor() as cursor:
                sql="SELECT ruta_archivo, nombre_archivo FROM foto WHERE evento_id=(%s) LIMIT 1;"
                cursor.execute(sql,id)
                resultado=cursor.fetchone()
                sql2="SELECT nombre FROM comuna WHERE id=(%s);"
                cursor.execute(sql2,comuna)
                result2=cursor.fetchall()

        finally: 
            print("<tr>")
            print("<td>"+str(dia_inicio)+"</td>")
            print("<td>"+str(dia_termino)+"</td>")
            print("<td>"+result2[0][0]+"</td>")
            print("<td>"+str(sector)+"</td>")
            print("<td>"+tipo+"</td>")
            print("<td>"+"<img width='320' height='240' src='"+resultado[0]+resultado[1]+"'></td>")
            print("</tr>")
    conn.close()

print("</table>")
print("</body></html>")
