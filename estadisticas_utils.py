from parser import *

def agarrar_datos_estadisticas_usuario(nombre_usuario:str) -> tuple:
    archivo_estadisticas = leer_archivo_json("configfiles/estadisticas.json")
    estadisticas_usuario = archivo_estadisticas[nombre_usuario]
    partidas_ganadas = estadisticas_usuario["partidas_ganadas"]
    aciertos_totales = estadisticas_usuario["aciertos_totales"]
    errores_totales = estadisticas_usuario["errores_totales"]
    rondas_totales = estadisticas_usuario["rondas_jugadas"]
    if rondas_totales > 0:
        tiempo_promedio_por_pregunta = estadisticas_usuario["tiempo_total"] / rondas_totales 
    else:
        tiempo_promedio_por_pregunta = 0
    return partidas_ganadas, aciertos_totales, errores_totales, rondas_totales, tiempo_promedio_por_pregunta