#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
import cgitb
import pymysql
from pymysql.cursors import Cursor

cgitb.enable()
print("Content-type: text/html; charset=UTF-8") # <-- Esto dice al interprete que es una pagina web
print('')
print("<html><head><link href='/~vasepulv/style.css' rel='stylesheet' type='text/css'></head>")
print("<body>")
#Body del HTML
lista=f"""
<table>
            <tr>
                <td><a href="/~vasepulv/cgi-bin/index.py"><button type="button">Portada</button></a></td>
                <td><a href="/~vasepulv/cgi-bin/form.py"><button type="button">Informar Evento</button></a></td>
                <td><a href="/~vasepulv/cgi-bin/list.py"><button type="button">Ver listado de Eventos</button></a></td>
                <td><a href="/~vasepulv/estadisticas.html"><button type="button">Estadísticas</button></a></td>
            </tr>
        </table>
"""

print(lista)

lista2="""
<h1>Listado de Eventos</h1>
        <table>
            <tr>
                <td>Fecha hora inicio</td>
                <td>Fecha hora término</td>
                <td>Comuna</td>
                <td>Sector</td>
                <td>tipo comida</td>
                <td>Nombre contacto</td>
                <td>total fotos</td>
            </tr>
"""
print(lista2)

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
        sql="SELECT id, comuna_id, sector, nombre, dia_hora_inicio, dia_hora_termino, tipo FROM evento;"
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
                <td>0</td>
            </tr>
    """
    print(value)

else:
    for id,comuna_id,sector,nombre,dia_hora_inicio,dia_hora_termino,tipo in result:
        result2=""
        result3=""
        conn=pymysql.connect(
            db="cc500263_db",
            port=3306,
            user="cc500263_u",
            passwd="ntesquesus",
            host="localhost"
        )
        result2=""
        result3=""
        try:
            with conn.cursor() as cursor:
                sql="SELECT COUNT(nombre_archivo) FROM foto WHERE evento_id=(%s);"
                cursor.execute(sql,id)
                result2=cursor.fetchall()

                sql2="SELECT nombre FROM comuna WHERE id=(%s);"
                cursor.execute(sql2,comuna_id)
                result3=cursor.fetchall()
        finally:
            if (sector==None):
                sector=" "
            print("<tr onclick='goToRef("+str(id)+");'>")
            print("<td>"+str(dia_hora_inicio)+"</td>")
            print("<td>"+str(dia_hora_termino)+"</td>")
            print("<td>"+result3[0][0]+"</td>")
            print("<td>"+sector+"</td>")
            print("<td>"+tipo+"</td>")
            print("<td>"+nombre+"</td>")
            print("<td>"+str(result2[0][0])+"</td>")
            print("</tr>")

print("</table>")

# El script de JS

funct="""
    <script language='JavaScript' type='text/javascript' src='/~vasepulv/listScript.js'>
    </script>
"""
print(funct)
print("</body></html>")