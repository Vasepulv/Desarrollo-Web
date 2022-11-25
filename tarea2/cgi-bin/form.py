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
# El body del HTML
body=f"""
<table>
        <tr>
                <td><a href="/~vasepulv/cgi-bin/index.py"><button type="button">Portada</button></a></td>
                <td><a href="/~vasepulv/cgi-bin/form.py"><button type="button">Informar Evento</button></a></td>
                <td><a href="/~vasepulv/cgi-bin/list.py"><button type="button">Ver listado de Eventos</button></a></td>
                <td><a href="/~vasepulv/estadisticas.html"><button type="button">Estadísticas</button></a></td>
        </tr>
</table>
"""
print(body)
print("<h1>Formulario</h1>")

forma=f"""
<form enctype="multipart/form-data" onsubmit="return verificar();" action="/~vasepulv/cgi-bin/validar.py" method="post">
            <h2>¿Dónde?:</h2>
            <label for="region">Selecciona la Región del evento.</label>
"""
print(forma)

conn=pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
)
region=""
comuna=""
try:
    with conn.cursor() as cursor:
        sql="SELECT DISTINCT id,nombre FROM region;"
        cursor.execute(sql)
        region=cursor.fetchall()
finally:
    conn.close()

print("<select id='region' name='region'>")

for id,name in region:
    print("<option value='"+str(id)+"'>"+str(name)+"</option>")

print("</select><br>")


com="""
<label for="comuna">Selecciona la comuna:</label>
            <select id="comuna" name="comuna" onclick='getComuna();'>
"""
print(com)

sector="""
            <label for="sector">Sector del evento:</label>
            <input type="text" maxlength="100" id="sector" name="sector" value="" size="100"><br>
            <h2 id="ofrece" name="ofrece">¿Quién ofrece?</h2>
"""
print(sector)

nombre="""
<label for="nombre">Nombre:</label>
            <input type="text" maxlength="200" id="nombre" name="nombre" value="" size="100"> <br>

            <label for="email">Email</label>
            <input type="email" id="email" name="email" size="100"><br>

            <label for="celular">Celular</label>
            <input type="text" size="15" name="celular" id="celular" value=""><br>
"""
print(nombre)

redes_sociales="""
    <label for="red-social">Redes Sociales</label>
            <select id="red-social" name="red-social" onclick="agregarRedSocial();">
                <option id="red-social0" value="Twitter">Twitter</option>
                <option id="red-social1" value="Instagram">Instagram</option>
                <option id="red-social2" value="Facebook">Facebook</option>
                <option id="red-social3" value="TikTok">Tiktok</option>
                <option id="red-social4" value="Otra">Otra</option>
            </select>
"""
print(redes_sociales)

tiempo="""
<h2>¿Cuándo y qué se ofrece?:</h2>

            <label for="dia-hora-inicio">Dia - Hora de Inicio</label>
            <input type="text" id="dia-hora-inicio" name="dia-hora-inicio" size="20" onclick="getTimeInicio()"><br>

            <label for="dia-hora-termino">Dia - Hora de Termino</label>
            <input type="text" id="dia-hora-termino" name="dia-hora-termino" size="20" onclick="getTimeTermino()"><br>

            <label for="descripcion-evento">Descripcion del Evento</label><br>
            <textarea id="descripcion-evento" name="descripcion-evento" rows="10" cols="100" value=""></textarea><br>
"""
print(tiempo)

tipo="""
    <label for="tipo-comida">Tipo de Comida:</label>
            <select id="tipo-comida" name="tipo-comida" onclick="agregarTipo();">
                <option value="0"></option>
            </select><br><br>
"""
print(tipo)

foto="""
    <label for="foto-comida">Foto de la Comida:</label>
    <button type="button" id="foto" name="foto" onclick="agregarFoto();">Agregar foto</button><br><br>
"""
print(foto)

validacion="<button type='submit'>Enviar información de este evento</button></form>"
print(validacion)


#El script del JS
print("<script type='text/javascript' language='JavaScript' src='/~vasepulv/formScript.js'>")
print("</script>")
print("</body></html>")
