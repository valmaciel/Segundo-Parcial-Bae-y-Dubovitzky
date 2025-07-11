from parser import *
from mensajes import inicializar_mensajes_estadisticas_usuario
from estadisticas_utils import *
from estadisticas_utils import *
import os

def mostrar_estadisticas():
    archivo_estadisticas = leer_archivo_json("configfiles/estadisticas.json")
    os.system("cls")
    for nombre in archivo_estadisticas:
        partidas_ganadas, aciertos_totales, errores_totales, rondas_totales, tiempo_promedio_por_pregunta = agarrar_datos_estadisticas_usuario(nombre)
        (
        mensaje_partidas_ganadas, mensaje_aciertos_totales, 
        mensaje_errores_totales, mensaje_rondas_totales, 
        mensaje_tiempo_promedio_por_pregunta
        ) = inicializar_mensajes_estadisticas_usuario(
        partidas_ganadas, aciertos_totales, 
        errores_totales, rondas_totales, 
        tiempo_promedio_por_pregunta
        )
        print("———————————————————————————————————————————————————————————————————————————————")
        print(f"Estadisticas de {nombre}:\n")
        print(mensaje_partidas_ganadas)
        print(mensaje_aciertos_totales)
        print(mensaje_errores_totales)
        print(mensaje_rondas_totales)
        print(mensaje_tiempo_promedio_por_pregunta)

