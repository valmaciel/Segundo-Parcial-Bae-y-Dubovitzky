from parser import *
from input import *
import random
import os
import time

def agregar_estadistica(usuario:str, estadistica:str, cantidad:float = 1):
    archivo_estadisticas = leer_archivo_json("configfiles/estadisticas.json")
    estadisticas_usuario = archivo_estadisticas[usuario]
    estadisticas_usuario[estadistica] += cantidad
    escribir_archivo_json(archivo_estadisticas, "configfiles/estadisticas.json")

def elegir_pregunta_random(dificultad:str):
    preguntas_diccionario = parser_csv()
    preguntas_de_dificultad = preguntas_diccionario[dificultad]
    id_random = random.randint(1, len(preguntas_de_dificultad))
    pregunta_electa = preguntas_de_dificultad[id_random]
    return pregunta_electa

def calcular_tiempo(inicio:float, final:float) -> float:
    tiempo_total = final - inicio
    return tiempo_total

def hacer_pregunta(preguntas_validas:list, vidas:int, dificultad:str, usuario:str, puntos_corona:int, categorias_restantes:list, modo_versus:bool = False, modo_corona:bool = False, categoria_electa:int = 0):
    random.shuffle(preguntas_validas)
    pregunta_actual = preguntas_validas.pop()
    os.system("cls")
    if modo_versus:
        print(f"Turno de: {usuario}")
        print(f"Puntos corona: {puntos_corona}")
    else:
        print("Vidas: " + " ❤️ " * vidas)
    print(f"\nDificultad: {dificultad}")
    print(f"Época: {pregunta_actual['categoria'].capitalize()}\n")
    print(pregunta_actual["pregunta"])
    opciones = pregunta_actual["opciones"]
    for i in range(len(opciones)):
        print(f"{chr(97 + i)}) {opciones[i]}")
    return pregunta_actual

def obtener_lista_preguntas_por_dificultad(dificultad:str, categoria:str = ""):
    preguntas_diccionario = parser_csv()
    
    # Para modo Versus
    if dificultad == "Versus":
        # Si es una ronda corona, filtramos por categoría
        if categoria:
            preguntas_filtradas = []
            for dificultad_nivel in preguntas_diccionario:
                for pregunta in preguntas_diccionario[dificultad_nivel]:
                    if pregunta['categoria'].lower() == categoria.lower():
                        preguntas_filtradas.append(pregunta)
            random.shuffle(preguntas_filtradas)
            return preguntas_filtradas
        # Si no es ronda corona, devolvemos todas las preguntas mezcladas
        else:
            todas_las_preguntas = []
            for dificultad_nivel in preguntas_diccionario:
                for pregunta in preguntas_diccionario[dificultad_nivel]:
                    todas_las_preguntas.append(pregunta)
            random.shuffle(todas_las_preguntas)
            return todas_las_preguntas
    
    # Para modo Arcade
    else:
        # Determinar dificultades permitidas según nivel seleccionado
        match dificultad:
            case "Fácil":
                dificultades_permitidas = ["1", "2"]
            case "Normal":
                dificultades_permitidas = ["1", "2", "3"]
            case "Difícil":
                dificultades_permitidas = ["2", "3", "4"]
        
        # Recolectar preguntas según dificultad permitida
        preguntas_validas = []
        for dificultad_nivel in dificultades_permitidas:
            if dificultad_nivel in preguntas_diccionario:
                preguntas_validas.extend(preguntas_diccionario[dificultad_nivel])
        
        # Mezclar las preguntas antes de devolverlas
        random.shuffle(preguntas_validas)
        return preguntas_validas
        
def obtener_y_validar_respuesta_pregunta(pregunta:dict):
    inicio_cronometro = time.time()
    respuesta_ingresada = obtener_opcion_letra("abcd", "Elija su respuesta: ", "Error de comprensión, elija su respuesta: ")
    final_cronometro = time.time()
    tiempo_total = calcular_tiempo(inicio_cronometro, final_cronometro)

    if respuesta_ingresada.lower() == pregunta["respuesta"].lower():
        bandera_correcto = True
    else:
        bandera_correcto = False
    return bandera_correcto, tiempo_total
def printear_pantalla_consola_estadisticas_partida(usuario1:str, rondas_jugadas_partida1:int, aciertos_partida1:int, errores_partida1:int, usuario2:str = "", rondas_jugadas_partida2:int = 0, aciertos_partida2:int = 0, errores_partida2:int = 0, usuario_ganador:str = "",  modo_versus = False):
    os.system("cls")
    if modo_versus:
        print(f"""Partida VERSUS terminada

        Ganador: {usuario_ganador} 🎉 🥳

        ———————————————————————————————————————————————————————            
        Jugador: {usuario1}

        Estadísticas partida:
        - Rondas jugadas: {rondas_jugadas_partida1}
        - Aciertos: {aciertos_partida1}
        - Errores: {errores_partida1}
        ———————————————————————————————————————————————————————
        Jugador: {usuario2}

        Estadísticas partida:
        - Rondas jugadas: {rondas_jugadas_partida2}
        - Aciertos: {aciertos_partida2}
        - Errores: {errores_partida2}
        ———————————————————————————————————————————————————————\n""") 
    else:
        print(f"""Partida ARCADE terminada
            
        Jugador: {usuario1}

        Estadísticas partida:
        - Rondas jugadas: {rondas_jugadas_partida1}
        - Aciertos: {aciertos_partida1}
        - Errores: {errores_partida1}\n""")
    input("Presiona ENTER para continuar... ")

def filtrar_por_categoria(categoria_deseada):
    preguntas_diccionario = parser_csv()
    diccionario_preguntas_final = {}

    for dificultad in preguntas_diccionario:
        preguntas = preguntas_diccionario[dificultad]
        filtradas = []

        for pregunta in preguntas:
            if pregunta['categoria'] == categoria_deseada:
                filtradas.append(pregunta)

        if len(filtradas) > 0:
            diccionario_preguntas_final[dificultad] = filtradas

    return diccionario_preguntas_final

def verificar_accesibilidad(opcion_accesibilidad:str):
    archivo_configuracion = leer_archivo_json("configfiles/config.json")
    bandera = False
    if archivo_configuracion["accesibilidad"][opcion_accesibilidad]:
        bandera = True
    return bandera

def agregar_monedas(usuario:str, cantidad:int):
    archivo_usuarios = leer_archivo_json()
    archivo_usuarios[usuario]["monedas"] += cantidad
    
