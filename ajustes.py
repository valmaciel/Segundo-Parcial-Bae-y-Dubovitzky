from input import *
from usuarios import *
from ajustes_utils import *
from mensajes import *
import time
import os

def mostrar_ajustes(usuario:str, password:str, bandera_premenu:bool = False):
    from menu import mostrar_menu_principal, mostrar_pre_menu
    os.system("cls")
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_ajustes()
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("123", "Su opción: ", "Error de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            mostrar_opciones_sonido(usuario, password, bandera_premenu)
        case 2:
            mostrar_opciones_accesibilidad(usuario, password, bandera_premenu)
        case 3:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(1)
            if bandera_premenu:
                mostrar_pre_menu()
            else:
                mostrar_menu_principal(usuario, password)
        case _:
            print("ERROR")

def mostrar_opciones_sonido(usuario:str, password:str, bandera_premenu:bool = False):
    os.system("cls")
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_sonido()
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("1234", "Su opción: ", "Error de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            subconfiguracion = "general"
            cambiar_volumen(subconfiguracion)
            mostrar_opciones_sonido(usuario, password, bandera_premenu)
            pass
        case 2:
            subconfiguracion = "musica"
            cambiar_volumen(subconfiguracion)
            mostrar_opciones_sonido(usuario, password, bandera_premenu)
            pass
        case 3:
            subconfiguracion = "efectos"
            cambiar_volumen(subconfiguracion)
            mostrar_opciones_sonido(usuario, password, bandera_premenu)
            pass
        case 4:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(1)
            mostrar_ajustes(usuario, password, bandera_premenu)
        case _:
            print("ERROR")

def mostrar_opciones_accesibilidad(usuario:str, password:str, bandera_premenu:bool = False):
    os.system("cls")
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_accesibilidad()
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("1234", "Su opción: ", "Error de lectura...\nSu opción: ")
    configuracion = "accesibilidad"
    match ingreso_usuario:
        case 1:
            subconfiguracion = "tdah"
            mostrar_opcion_toggleable(configuracion, subconfiguracion, usuario, password)
        case 2:
            mostrar_opciones_daltonismo(usuario, password)
        case 3:
            subconfiguracion = "tea"
            mostrar_opcion_toggleable(configuracion, subconfiguracion, usuario, password)
        case 4:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(1)
            mostrar_ajustes(usuario, password, bandera_premenu)
        case _:
            print("ERROR")

def mostrar_opcion_toggleable(configuracion:str, subconfiguracion:str, usuario:str, password:str, bandera_premenu:bool = False):
    os.system("cls")
    archivo = leer_archivo_json("configfiles/config.json")
    estado = archivo[configuracion][subconfiguracion]
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_accesibilidad_toggle(subconfiguracion, estado)
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("123", "Su opción: ", "Error de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            toggle_booleano_json(configuracion, subconfiguracion, True)
            mostrar_opcion_toggleable(configuracion, subconfiguracion, usuario, password)
        case 2:
            toggle_booleano_json(configuracion, subconfiguracion, False)
            mostrar_opcion_toggleable(configuracion, subconfiguracion, usuario, password)
        case 3:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(1)
            mostrar_opciones_accesibilidad(usuario, password, bandera_premenu) 
        case _:
            print("ERROR")

def mostrar_opciones_daltonismo(usuario:str, password:str, bandera_premenu:bool = False):
    os.system("cls")
    archivo = leer_archivo_json("configfiles/config.json")
    estado_daltonismo = archivo["accesibilidad"]["daltonismo"]
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_accesibilidad_daltonismo(estado_daltonismo)
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("12345", "Su opción: ", "Error de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            tipo_de_daltonismo = "protanopia"
            cambiar_opcion_daltonismo(tipo_de_daltonismo)
            mostrar_opciones_daltonismo(usuario, password, bandera_premenu)
        case 2:
            tipo_de_daltonismo = "deuteranopia"
            cambiar_opcion_daltonismo(tipo_de_daltonismo)
            mostrar_opciones_daltonismo(usuario, password, bandera_premenu)
        case 3:
            tipo_de_daltonismo = "tritanopia"
            cambiar_opcion_daltonismo(tipo_de_daltonismo)
            mostrar_opciones_daltonismo(usuario, password, bandera_premenu)
        case 4:
            tipo_de_daltonismo = "ninguno"
            cambiar_opcion_daltonismo(tipo_de_daltonismo)
            mostrar_opciones_daltonismo(usuario, password, bandera_premenu)
        case 5:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(1)
            mostrar_opciones_accesibilidad(usuario, password, bandera_premenu) 
        case _:
            print("ERROR")

def cambiar_volumen(subconfiguracion:str):
    os.system("cls")
    archivo_config = leer_archivo_json("configfiles/config.json")
    print(f"Opcion de volumen: {subconfiguracion.upper()}\n")
    print(f"Actualmente está en: {archivo_config["volumen"][subconfiguracion]}\n")
    volumen_deseado = obtener_numero_0_al_100()
    cambiar_opcion_sonido(subconfiguracion, volumen_deseado)


