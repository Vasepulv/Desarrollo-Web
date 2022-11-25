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

id=dict.getvalue('evento-id')


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
        sql="SELECT comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo FROM evento WHERE id=(%s);"
        cursor.execute(sql,id)
        result=cursor.fetchall()
finally:
    conn.close()

print("<h1>"+"Evento "+id+"</h1>")


conn2=pymysql.connect(
        db="cc500263_db",
        port=3306,
        user="cc500263_u",
        passwd="ntesquesus",
        host="localhost"
    )

for comuna_id,sector,nombre,email,celular,dia_hora_inicio,dia_hora_termino,descripcion,tipo in result:
    result2=""
    result3=""
    result4=""
    try:
        with conn2.cursor() as cursor:
            sql="SELECT region_id,nombre FROM comuna WHERE id=(%s);"
            cursor.execute(sql,comuna_id)
            result2=cursor.fetchone()

            sql2="SELECT nombre FROM region WHERE id=(%s);"
            cursor.execute(sql2,result2[0])
            result3=cursor.fetchone()

            sql3="SELECT id, ruta_archivo, nombre_archivo, evento_id FROM foto WHERE evento_id=(%s);"
            cursor.execute(sql3,id)
            result4=cursor.fetchone()
    finally:
        print("<h3>¿Donde?</h3>")
        print("<p>Región: "+result3[0]+"</p>")
        print("<p>Comuna: "+result2[1]+"</p>")
        print("<p>Sector: "+sector+"</p>")
        print("<h3>¿Quién ofrece?</h3>")
        print("<p>Nombre Contacto: "+nombre+"</p>")
        print("<p>Email: "+email+"</p>")
        print("<p>Celular: "+celular+"</p>")
        print("<p>Redes Sociales: </p>")
        print("<h3>¿Cuándo y qué se ofrece?</h3>")
        print("<p>Dia hora inicio: "+str(dia_hora_inicio)+"</p>")
        print("<p>Dia hora termino: "+str(dia_hora_termino)+"</p>")
        print("<p>Descripción evento: "+descripcion+"</p>")
        print("<p>Tipo de Comida: "+tipo+"</p>")
        print("<p><b>Fotos Comida:</b></p>")
        print("<a href='foto.py?foto-id="+str(result4[0])+"'>"+"<img src='"+result4[1]+result4[2]+"' width='320' height='240'></a><br><br>")

        print("""
        <a href="list.py"><button type="button">Regresar al Listado</button></a>
        <a href="index.py"><button type="button">Regresar a la Portada</button></a>
        </body>
        </html>""")
    
