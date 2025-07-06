import re
import json

def parser_csv(nombre_archivo='preguntas.csv'):
    preguntas_por_categoria = {}
    try:
        with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
            bandera_primera_linea = True
            for linea in archivo_csv:
                if bandera_primera_linea:
                    bandera_primera_linea = False
                    continue
                pregunta = {}
                registro = re.split(",|\r", linea)
                categoria = registro[0]
                pregunta['pregunta'] = registro[1]
                opcion_a = registro[2]
                opcion_b = registro[3]
                opcion_c = registro[4]
                opcion_d = registro[5]
                pregunta['opciones'] = [opcion_a,opcion_b,opcion_c,opcion_d]
                pregunta['respuesta'] = registro[6]
                if categoria not in preguntas_por_categoria:
                    preguntas_por_categoria[categoria] = []
                preguntas_por_categoria[categoria].append(pregunta)
    except:
        pass
    
    return preguntas_por_categoria

def cargar_datos_json(lista_usuarios:dict):
    with open("usuarios_config.json", "w") as archivo:
        json.dump(lista_usuarios, archivo, indent=4)

def parser_json():
    with open("usuarios_config.json", "r") as archivo:
        lista_usuarios = json.load(archivo)
    return lista_usuarios