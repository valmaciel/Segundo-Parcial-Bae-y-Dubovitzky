from input import *
from usuarios import *
from ajustes import mostrar_ajustes
from mensajes import inicializar_mensajes_menu_principal, inicializar_mensajes_pre_menu
from estadisticas import *
from juego_arcade import *
from juego_versus import *
import time
import os

def mostrar_menu_principal(usuario:str, password:str):
    os.system("cls")
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_menu_principal(usuario)
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("12345", "Su opción: ", "\rError de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            menu_arcade(usuario, password)
        case 2:
            jugar_versus(usuario, password)
        case 3:
            mostrar_estadisticas()
            print("———————————————————————————————————————————————————————————————————————————————")
            input("\nPresionar ENTER para continuar...")
            mostrar_menu_principal(usuario, password)
        case 4:
            mostrar_ajustes(usuario, password)
        case 5:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(2)
            mostrar_pre_menu()
        case _:
            print("ERROR")

def mostrar_pre_menu():
    os.system("cls")
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_pre_menu()
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("1234", "Su opción: ", "Error de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            usuario, password = iniciar_sesion_consola()
            mostrar_menu_principal(usuario, password)
        case 2:
            registrar_usuario_consola()
            mostrar_pre_menu()
        case 3:
            mostrar_ajustes("", "", bandera_premenu = True)
        case 4:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(2)
            quit()
        case _:
            print("ERROR")

