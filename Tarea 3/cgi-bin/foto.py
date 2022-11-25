#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import filetype
import pymysql
from pymysql.cursors import Cursor

cgitb.enable()
print("Content-type: text/html; charset=UTF-8") # <-- Esto dice al interprete que es una pagina web
print('')
print("<html><head><link href='/~vasepulv/style.css' rel='stylesheet' type='text/css'></head>")
print("<body>")


dict=cgi.FieldStorage()
id=dict.getvalue("foto-id")

conn=pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
)

try:
    result=""
    with conn.cursor() as cursor:
        sql="SELECT ruta_archivo, nombre_archivo,evento_id FROM foto WHERE id=(%s);"
        cursor.execute(sql,id)
        result=cursor.fetchone()
        print(result[2])

finally:
    conn.close()
    print("<img width='800' height='600' src='"+result[0]+result[1]+"'>")
    print("<a href='evento.py?evento-id="+str(result[2])+"'><button type='button'>Volver</button></a>")

print("</body>")
print("</html>")

