import random
import time
import os
from usuarios import *
from generales import *
from input import *
from parser import *

def girar_rueda(ciclos=2, delay=0.5):
    for i in range(ciclos):
        for puntos in range(1, 4):
            print(f'\r🎡 Girando la rueda {"." * puntos}   ', end='')
            time.sleep(delay)

def obtener_categoria_aleatoria(lista_categorias):
    categoria_elegida = random.choice(lista_categorias)
    return categoria_elegida

def hacer_pregunta(categoria:str, pregunta:str, opciones:list):
    girar_rueda()
    print ("\033[A                                                                                                   \033[A")
    print(f'\nCategoría: {categoria}            ')
    print(pregunta)
    for i in range(len(opciones)):
        print(f'{chr(97 + i)}) {opciones[i]}')

def calcular_puntos_coronas(categoria_electa, puntos_corona):
    bandera_ronda_corona = False
    if categoria_electa == 'Corona' or puntos_corona >= 3:
        bandera_ronda_corona = True
    return bandera_ronda_corona

def convertir_respuesta_a_categoria(ingreso:str, diccionario_mapeo_categorias:dict):
    categoria_en_string = diccionario_mapeo_categorias[ingreso]
    return categoria_en_string

def elegir_numero_de_pregunta_aleatorio(diccionario_con_preguntas:dict, categoria:str):
    cantidad_preguntas = len(diccionario_con_preguntas[categoria])
    numero_de_pregunta_random = random.randint(0, cantidad_preguntas - 1)
    return numero_de_pregunta_random

def verificar_categoria_restante(jugador, categorias_por_letra, categoria_electa):
    while not buscar_variable_en_lista(categoria_electa, jugador['categorias_restantes']):
        print(f'Error... Ya tienes la corona de esa categoría\nCategorías restantes: {jugador['categorias_restantes']}')
        categoria_electa_por_jugador = obtener_respuesta(['a','b','c','d','e','f'])
        categoria_electa = convertir_respuesta_a_categoria(categoria_electa_por_jugador, categorias_por_letra)
    return categoria_electa

def mandar_tiempo(tiempo, jugador):
    jugador['rondas_jugadas'] += 1
    jugador['tiempo_total'] += tiempo
    jugador['promedio_tiempo_por_ronda'] = jugador['tiempo_total'] / jugador['rondas_jugadas']

def mostrar_estadisticas():
    archivo = parser_json()
    os.system('cls')
    lista_jugadores = archivo['jugadores']
    for i in range(len(lista_jugadores)):
        print(f"Jugador: {lista_jugadores[i]['nombre']}")
        print(f" - Tiempo promedio por ronda: {(lista_jugadores[i]['promedio_tiempo_por_ronda'])}")
        print(f" - Rondas jugadas: {(lista_jugadores[i]['rondas_jugadas'])}")
        print(f" - Aciertos: {(lista_jugadores[i]['aciertos_totales'])}")
        print(f" - Errores: {(lista_jugadores[i]['errores_totales'])}")
        print(f" - Coronas totales (partidas ganadas): {(lista_jugadores[i]['wins'])}")
        print("\n---------------------------------------------------------------------\n")
    input('Presiona ENTER para salir')

def cambiar_aspecto(usuario, password):
    os.system('cls')
    id_usuario = obtener_id_usuario(usuario, password)
    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    print('Ingrese su aspecto deseado (0-4)\n')
    aspecto_nuevo = obtener_respuesta_1('12345')
    lista_usuarios[id_usuario]['aspecto'] = aspecto_nuevo
    cargar_datos_json(archivo)

def agregar_acierto_o_error(usuario:str, password:str, acierto:bool = True):
    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    usuario_id = obtener_id_usuario(usuario, password)
    if acierto:
        lista_usuarios[usuario_id]['aciertos_totales'] += 1
    elif not acierto:
        lista_usuarios[usuario_id]['errores_totales'] += 1
    cargar_datos_json(archivo)

def agregar_todas_las_categorias():
    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    for i in range(len(lista_usuarios)):
        lista_usuarios[i]['categorias_restantes'] = [
            "Historia",
            "Ciencia",
            "Geografía",
            "Arte",
            "Deportes",
            "Entretenimiento"
        ]
    cargar_datos_json(archivo)





# Consigna importante:
# - Estadisticas (modo facil)
# - Estadisticas (pregunta mas errada)
# - Estadisticas (aciertos y errores totales)

# Bugs y errores de concepto:
# - Menu pre-login y principal