#! /usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
from typing import List
import pymysql
import re
import os
import filetype
from PIL import Image


cgitb.enable()
print("Content-type: text/html; charset=UTF-8") # <-- Esto dice al interprete que es una pagina web
print('')
print("<html><head><link href='/~vasepulv/style.css' rel='stylesheet' type='text/css'></head>")

tipo_comida=["Al Paso", "Alemana", "Árabe"
                "Argentina","Australiana","Brasileña","Café y Snacks","Carnes","Chilena","China"
                ,"Cocina de Autor","Comida Rápida","Completos","Coreana","Cubana","Española","Exótica","Francesa","Gringa"
                ,"Hamburguesa","Helados","India","Internacional","Italiana","Latinoamericana","Mediterránea","Mexicana"
                ,"Nikkei","Parrillada","Peruana","Pescados y mariscos","Picoteos","Pizzas","Pollos y Pavos","Saludable"
                ,"Sándwiches","Suiza","Japonesa","Sushi","Tapas","Thai","Vegana","Vegetariana"]

def validarRegion(region,comuna):
    isCorrect=True
    conn=pymysql.connect(
        db="cc500263_db",
        port=3306,
        user="cc500263_u",
        passwd="ntesquesus",
        host="localhost"
    )
    try:
        with conn.cursor() as cursor:
            sql="SELECT region_id FROM comuna WHERE AND nombre=(%s);"
            cursor.execute(sql,(comuna))
            result=cursor.fetchone()
            print(result)
            if (result['region_id']==region):
                isCorrect=False
    finally:
        conn.close()
        return isCorrect


def validarNombre(nombre):
    nom=nombre.upper()
    return (len(nom)>0 and len(nom)<100)

def validarCelular(celular):
    if (celular==""):
        return True
    celular2=str(celular)
    isCorrect=celular2.isnumeric()
    if celular2.isnumeric()==True:
        return len(celular2)>8 and len(celular2)<15
    isCorrect=(celular2.index(0)=='+' and celular2.replace('+',"").isnumeric())
    return (isCorrect and len(celular2)>8 and len(celular2)<15)

def validarEmail(email):
    rex=re.compile('\w+@\w+\.com')
    rex2=re.compile('\w+@\w+\.cl')
    return ((len(re.findall(rex,email))>0 or len(re.findall(rex2,email))>0 ) and len(email)<100)

def validarTiempo(tiempo):
    rex=re.compile('\d\d\d\d-\d\d-\d\d\s\d\d:\d\d')
    rex2=re.compile('\d\d\d\d-\d-\d\d\s\d\d:\d\d')
    if (rex.search(tiempo)!=None):
        return True
    if (rex2.search(tiempo)!=None):
        return True
    return False

def validarTipo(tipo):
    return (tipo in tipo_comida)

def validarDescripcion(descripcion):
    if (descripcion==None):
        return True
    return len(descripcion)<500

def validarSector(sector):
    if (sector==None):
        return True
    return (len(sector)<100)

def validarRedSocial(red, url):
    isCorrect=True
    j=0
    for r in red:
        if (r==None):
            return True
        rex=re.compile('/\w+/')
        containsUrl=url[j].startswith("https://www.")
        index=url.rfind(r+".com")
        isCorrect=isCorrect and index>9 and len(re.findall(rex,url[0]))>0 and containsUrl
        j=j+1
    return isCorrect

def validarFotos(fotos):
    mensaje=""
    for foto in fotos:
        if (foto.filename):
            try:
                type=filetype.guess_extension(foto.file)
                fn=os.path.basename(foto.filename)
                open('/tmp/'+fn,'wb').write(foto.file.read())
                if (type==None):
                    return False
                if (type=="jpg" or type=="png"):
                    mensaje="Es una foto"
            except IOError as e:
                mensaje = "Error al obtener informacion de archivo"
                return False
                
        else:
            print("No es una foto valida")
            return False
    print(mensaje)
    return True  

dict=cgi.FieldStorage()

#Validar region
region=dict.getvalue('region')

#validar comuna
comuna=dict.getvalue('comuna')

#validar nombre
nombre=dict.getvalue('nombre')

#validar celular
celular=dict.getvalue('celular')

#Validar email
email=dict.getvalue('email')

#validar sector
sector=dict.getvalue('sector')

#validar hora-inicio
dia_hora_inicio=dict.getvalue('dia-hora-inicio')

#validar hora-termino
dia_hora_termino=dict.getvalue('dia-hora-termino')

#validar tipo
tipo_comida=dict.getvalue('tipo-comida')

#validar redes sociales
red_social=dict['red-social']

#validar descripcion
descripcion_evento=dict.getvalue('descripcion-evento')

#validar fotos
foto=dict['foto-comida']

fotos=[]
if (isinstance(foto,list)):
    fotos=foto
else:
    fotos.append(foto)


#validar red social
red=[]
redes=[]
if (isinstance(red_social,list)):
    redes=red_social
else:
    redes.append(red_social)



conn=pymysql.connect(
    db="cc500263_db",
    port=3306,
    user="cc500263_u",
    passwd="ntesquesus",
    host="localhost"
)

try:
    with conn.cursor() as cursor:
        sql="SELECT DISTINCT id FROM region where id=(%s);"
        cursor.execute(sql,region)
        result=cursor.fetchall()
finally:
    conn.close()


valRegion=validarRegion(region,comuna)
valNombre=validarNombre(nombre)
valCelular=validarCelular(celular)
valEmail=validarEmail(email)
valSector=validarSector(sector)
valTipo=validarTipo(tipo_comida)
valDesc=validarDescripcion(descripcion_evento)
valHI=validarTiempo(dia_hora_inicio)
valHT=validarTiempo(dia_hora_termino)
valRed=validarRedSocial(red,redes)
valFotos=validarFotos(fotos)
valido=valRegion and valNombre and valCelular and valEmail and valSector and valTipo and valDesc and valHI and valHT and valRed and valFotos

if (valido==False):
    print("<html>")
    print("<head>")
    print("<meta char-set=utf-8>")
    print("<title>Error</title>")
    print("<body>")
    print("<h2> Hay errores en el formulario</h2>")
    if (valRegion==False):
        print("<h3>Hay errores en la Region</h3>")
    if (valNombre==False):
        print("<h3>Hay errores con el nombre</h3>")
    if (valCelular==False):
        print("<h3>Hay errores con el formato del celular></h3>")
    if (valEmail==False):
        print("<h3>Hay errores con el email</h3>")
    if (valSector==False):
        print("<h3>Hay errores con el Sector</h3>")
    if (valTipo==False):
        print("<h3>Hay errores con el tipo</h3>")
    if(valDesc==False):
        print("<h3>Hay errores con la descripcion</h3>")
    if (valHI==False or valHT==False):
        print("<h3>Hay errores con el formato del Tiempo</h3>")
    if (valRed==False):
        print("<h3>Hay errores con la red-social</h3>")
    if (valFotos==False):
        print("<h3>Hay errores con la foto</h3>")
    print("</body></html>")
else:
    conn2=pymysql.connect(
        db="cc500263_db",
        port=3306,
        user="cc500263_u",
        passwd="ntesquesus",
        host="localhost"
    )
    try:
        with conn2.cursor() as cursor:
            sql11="SELECT id FROM comuna WHERE nombre=(%s);"
            cursor.execute(sql11,comuna)
            result=cursor.fetchall()
            comuna_id=result[0][0]
            sql2="INSERT INTO evento (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql2,(comuna_id,sector,nombre,email,celular,dia_hora_inicio,dia_hora_termino,descripcion_evento,tipo_comida))
            #result=cursor.fetchone()
            result==None
            cursor.execute("SELECT id FROM evento ORDER BY id DESC;")
            result=cursor.fetchall()
            if (result!=None and result!=()):
                print("Se insertó un evento")

                #print(redes)
                #print(red)
                #if (red_social[0]!=None):
                #    for i in redes:
                #        sql4="INSERT INTO red_social (nombre, identificador, evento_id) VALUES (%s, %s, %s);"
                #        cursor.execute(sql4,(i,red[i],result[0][0]))
                #        result3=cursor.fetchall()
                #        print(result3)
                #        print("Se pudo insertar")

                result2=""
                for foto in fotos:
                    sql3="INSERT INTO foto (ruta_archivo, nombre_archivo, evento_id) VALUES (%s, %s, %s)"
                    nombreArchivo=foto.filename
                    cursor.execute(sql3,("../image/",nombreArchivo,result[0][0]))
                    result2=cursor.fetchall()
                    conn2.commit()
                    if (result2==None):
                        print("No se pudo insertar la foto")
                    else:
                        print("Si se pudo insertar exitosamente")
                    fn=os.path.basename(nombreArchivo)
                    file=open("../image/"+fn,"w")
                    file.close()
                    picture=Image.open(foto.file)
                    picture=picture.save("../image/"+fn)
                
            else:
                conn2.rollback()
                print("Este evento ya está en el sistema, o hubo un error.")
                

            #conn2.commit()

    finally:
        conn2.close()

