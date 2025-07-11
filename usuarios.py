from parser import *
from input import *
import os

def crear_usuario(usuario:str, password:str) -> None:
    usuarios_diccionario = leer_archivo_json()
    usuarios_diccionario[usuario] = {
        "password": password,
        "monedas": 0,
        "items_comprados": []
    }
    escribir_archivo_json(usuarios_diccionario)
    
def crear_estadisticas(usuario:str) -> None:
    estadisticas_usuario = leer_archivo_json("configfiles/estadisticas.json")
    estadisticas_usuario[usuario] = {
        "partidas_ganadas": 0,
        "aciertos_totales": 0,
        "errores_totales": 0,
        "tiempo_total": 0,
        "rondas_jugadas": 0,
        "puntos_totales": 0
    }
    escribir_archivo_json(estadisticas_usuario, "configfiles/estadisticas.json")

def registrar_usuario(usuario:str, password:str) -> None:
    crear_usuario(usuario, password)
    crear_estadisticas(usuario)

def verificar_existencia_usuario(usuario:str) -> bool:
    usuarios_diccionario = leer_archivo_json()
    bandera = False
    for clave in usuarios_diccionario:
        if usuario == clave:
            bandera = True
    return bandera

def obtener_datos_usuario_nuevo_consola() -> tuple:
    nombre_usuario_nuevo = obtener_cadena("Ingrese su nombre de usuario: ", "Error, usuario no válido, ingrese de vuelta: ")
    while verificar_existencia_usuario(nombre_usuario_nuevo):
        print("Error: Nombre de usuario ya existe.")
        nombre_usuario_nuevo = obtener_cadena("Ingrese su nombre de usuario: ", "Error, usuario no válido, ingrese de vuelta: ")
    password_usuario_nuevo_1 = obtener_cadena("Ingrese su contraseña: ", "Error, contraseña no válida, ingrese de vuelta: ")
    password_usuario_nuevo_2 = obtener_cadena("Ingrese su de vuelta contraseña: ", "Error, contraseña no válida, ingrese de vuelta: ")
    while not verificar_cadenas_iguales(password_usuario_nuevo_1, password_usuario_nuevo_2):
        print("Error: Las contraseñas no coinciden.")
        password_usuario_nuevo_1 = obtener_cadena("Ingrese su contraseña: ", "Error, contraseña no válida, ingrese de vuelta: ")
        password_usuario_nuevo_2 = obtener_cadena("Ingrese su de vuelta contraseña: ", "Error, contraseña no válida, ingrese de vuelta: ")
    return nombre_usuario_nuevo, password_usuario_nuevo_1

def registrar_usuario_consola() -> None:
    os.system("cls")
    user_nuevo, pass_nuevo = obtener_datos_usuario_nuevo_consola()
    registrar_usuario(user_nuevo, pass_nuevo)
    print("¡Usuario registrado exitosamente!")

def iniciar_sesion(usuario, password) -> bool:
    usuarios_diccionario = leer_archivo_json()
    bandera_sesion_validada = False
    for clave in usuarios_diccionario:
        if clave == usuario:
            if password == usuarios_diccionario[usuario]["password"]:
                bandera_sesion_validada = True
    return bandera_sesion_validada

def iniciar_sesion_consola() -> tuple:
    os.system("cls")
    usuario_ingresado = obtener_cadena("Ingrese usuario: ", "Error, usuario no válido, ingrese usuario: ")
    password_ingresado = obtener_cadena("Ingrese su contraseña: ", "Error, contraseña no válida, ingrese de vuelta: ")
    while not iniciar_sesion(usuario_ingresado, password_ingresado):
        os.system("cls")
        print("Error: Usuario no existe.")
        usuario_ingresado = obtener_cadena("Ingrese usuario: ", "Error, usuario no válido, ingrese usuario: ")
        password_ingresado = obtener_cadena("Ingrese su contraseña: ", "Error, contraseña no válida, ingrese de vuelta: ")
    return usuario_ingresado, password_ingresado

def iniciar_sesion_consola_restringido(usuario1:str):
    usuario2, password2 = iniciar_sesion_consola()
    while usuario1 == usuario2:
        print("ERROR: Usuario no puede jugar contra sí mismo.")
        usuario2, password2 = iniciar_sesion_consola()
    return usuario2, password2