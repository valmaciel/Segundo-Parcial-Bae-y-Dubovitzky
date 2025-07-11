import re
import json

def parser_csv(nombre_archivo: str = "configfiles/preguntas.csv") -> dict:
    preguntas_por_dificultad = {}
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
        bandera_primera_linea = True
        for linea in archivo_csv:
            if bandera_primera_linea:
                bandera_primera_linea = False
                continue
            registro = re.split(",|\r", linea)
            dificultad = registro[8]
            pregunta = {
                'pregunta': registro[2],
                'opciones': [registro[3], registro[4], registro[5], registro[6]],
                'respuesta': registro[7],
                'categoria': registro[1],
                'puntaje': registro[9]
            }
            if dificultad not in preguntas_por_dificultad:
                preguntas_por_dificultad[dificultad] = []
            preguntas_por_dificultad[dificultad].append(pregunta)
    return preguntas_por_dificultad

def escribir_archivo_json(lista_usuarios:dict, archivo_nombre:str = "configfiles/usuarios.json"):
    with open(archivo_nombre, "w") as archivo:
        json.dump(lista_usuarios, archivo, indent=4)

def leer_archivo_json(archivo_nombre:str = "configfiles/usuarios.json"):
    with open(archivo_nombre, "r") as archivo:
        lista_usuarios = json.load(archivo)
    return lista_usuarios

