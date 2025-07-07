from parser import *
import os

def crear_usuario(nombre:str, password:str):
    usuario = {
        "nombre": nombre,
        "contra": password,
        "rondas_jugadas": 0,
        "aspecto": 0,
        "tiempo_total": 0,
        "promedio_tiempo_por_ronda": 0,
        "aciertos_totales": 0,
        "errores_totales": 0,
        "puntos": 0,
        "puntos_corona": 0,
        "wins": 0,
        "categorias_restantes": [
            "Historia",
            "Ciencia",
            "Geografía",
            "Arte",
            "Deportes",
            "Entretenimiento"
        ]
            }
    return usuario

def agregar_usuario(lista_usuarios:list, usuario_nuevo:dict):
    lista_usuarios.append(usuario_nuevo)

def verificar_repeticion_usuarios(lista_usuarios:list, nombre_nuevo:str):
    bandera = False
    for i in range(len(lista_usuarios)):
        if lista_usuarios[i]["nombre"] == nombre_nuevo:
            bandera = True
    return bandera

def loguear_usuario(lista_usuarios) -> tuple:
    bandera_login = False
    while not bandera_login:
        usuario_ingresado = input("Ingrese usuario: ")
        password_ingresado = input("Ingrese contraseña: ")
        for i in range(len(lista_usuarios)):
            if (lista_usuarios[i]["nombre"] == usuario_ingresado) and (lista_usuarios[i]["contra"] == password_ingresado):
                bandera_login = True
        if not bandera_login:
            os.system('cls')
            print("Error, usuario o contraseña ingresado/a es incorrecto/a...")

    return usuario_ingresado, password_ingresado

def obtener_id_usuario(usuario:str, contra:str) -> dict:
    datos = parser_json()
    lista_usuarios = datos["jugadores"]
    for i in range(len(lista_usuarios)):
        if (lista_usuarios[i]["nombre"] == usuario) and (lista_usuarios[i]["contra"] == contra):
            usuario_id = i
    return usuario_id

def registrar_usuario():
    usuarios = parser_json()
    bandera_pass_verificado = False
    lista_usuarios = usuarios["jugadores"]
    nombre_usuario_nuevo = input("Ingrese el nombre para el nuevo usuario: ")
    while verificar_repeticion_usuarios(lista_usuarios, nombre_usuario_nuevo):
        nombre_usuario_nuevo = input("Error, nombre ya utilizado...\nIngrese el nombre para el nuevo usuario: ")
    while not bandera_pass_verificado:
        pass_usuario_nuevo1 = input("Ingrese la contraseña del usuario nuevo: ")
        pass_usuario_nuevo2 = input("Ingrese la contraseña de nuevo: ")
        if pass_usuario_nuevo1 == pass_usuario_nuevo2:
            pass_usuario_nuevo = pass_usuario_nuevo1
            bandera_pass_verificado = True
        else: 
            print("Error, contraseña no coincide. Intente de nuevo \n")
        
    nuevo_usuario = crear_usuario(nombre_usuario_nuevo, pass_usuario_nuevo)
    agregar_usuario(lista_usuarios, nuevo_usuario)
    cargar_datos_json(usuarios)
    print("¡Operación realizada exitosamente!\n")
