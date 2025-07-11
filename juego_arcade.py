from parser import *
from juego_utils import *
from mensajes import inicializar_mensajes_menu_arcade
from input import *
import os
import time
import random

def menu_arcade(usuario:str, password:str):
    from menu import mostrar_menu_principal
    os.system("cls")
    mensaje_bienvenido, mensaje_opciones, mensaje_salida = inicializar_mensajes_menu_arcade(usuario)
    print(f"{mensaje_bienvenido}\n")
    print(mensaje_opciones)
    ingreso_usuario = obtener_opcion_numero("1234", "Su opción: ", "\rError de lectura...\nSu opción: ")
    match ingreso_usuario:
        case 1:
            dificultad = "Fácil"
            jugar_arcade(usuario, dificultad)
            menu_arcade(usuario, password)
        case 2:
            dificultad = "Normal"
            jugar_arcade(usuario, dificultad)
            menu_arcade(usuario, password)
        case 3:
            dificultad = "Difícil"
            jugar_arcade(usuario, dificultad)
            menu_arcade(usuario, password)
        case 4:
            os.system("cls")
            print(mensaje_salida)
            time.sleep(2)
            mostrar_menu_principal(usuario, password)
        case _:
            print("ERROR")

def jugar_pregunta_arcade(usuario:str, dificultad:str, vidas:int, rondas_jugadas_partida:int, aciertos_partida:int, errores_partida:int) -> bool:
    preguntas_validas = obtener_lista_preguntas_por_dificultad(dificultad)
    pregunta_actual = hacer_pregunta(preguntas_validas, vidas, dificultad, usuario, 0, categorias_restantes = [])
    bandera_correcto, tiempo_total = obtener_y_validar_respuesta_pregunta(pregunta_actual)
    if bandera_correcto:
        print("\n✅ ¡Correcto!")
        aciertos_partida += 1
        agregar_estadistica(usuario, "aciertos_totales")
    else:
        print("\n❌ Incorrecto...")
        errores_partida += 1
        agregar_estadistica(usuario, "errores_totales")
        vidas -= 1
    rondas_jugadas_partida += 1
    agregar_estadistica(usuario, "rondas_jugadas")
    agregar_estadistica(usuario, "tiempo_total", tiempo_total)
    input("\nPresiona ENTER para continuar... ")
    return vidas, rondas_jugadas_partida, aciertos_partida, errores_partida

def jugar_arcade(usuario:str, dificultad:str):
    vidas = 3
    rondas_jugadas_partida = 0
    aciertos_partida = 0
    errores_partida = 0
    while vidas > 0:
        vidas, rondas_jugadas_partida, aciertos_partida, errores_partida = jugar_pregunta_arcade(usuario, dificultad, vidas, rondas_jugadas_partida, aciertos_partida, errores_partida)
    printear_pantalla_consola_estadisticas_partida(usuario, rondas_jugadas_partida, aciertos_partida, errores_partida)

