import re
import json
import logging
from pathlib import Path    

logging.basicConfig(level=logging.ERROR, format="%(levelname)s | %(message)s")


def parser_csv(nombre_archivo: str = "preguntas.csv") -> dict:
    preguntas_por_categoria = {}
    try:
        with open(nombre_archivo, newline="", encoding="utf-8") as archivo_csv:
            primera_linea = True
            for linea in archivo_csv:
                if primera_linea:
                    primera_linea = False
                    continue

                registro = re.split(",|\r?\n", linea)
                registro = [campo for campo in registro if campo != '']

                if len(registro) >= 7:
                    categoria = registro[0]
                    pregunta = registro[1]
                    opciones = [registro[2], registro[3], registro[4], registro[5]]
                    respuesta = registro[6]

                    if categoria not in preguntas_por_categoria:
                        preguntas_por_categoria[categoria] = []

                    preguntas_por_categoria[categoria].append({
                        "pregunta": pregunta,
                        "opciones": opciones,
                        "respuesta": respuesta
                    })
                else:
                    logging.warning(f"Línea malformada ignorada: {linea!r}")

    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {nombre_archivo}")
    except Exception as e:
        logging.exception(f"Error procesando el CSV: {e}")

    return preguntas_por_categoria


def cargar_datos_json(lista_usuarios: dict, nombre_archivo: str = "usuarios_config.json") -> None:
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(lista_usuarios, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"No se pudo guardar el archivo JSON: {e}")


def parser_json(nombre_archivo: str = "usuarios_config.json") -> dict:
    lista_usuarios = {}

    try:
        if Path(nombre_archivo).exists():
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                lista_usuarios = json.load(archivo)
        else:
            logging.warning(f"El archivo {nombre_archivo} no existe.")
    except json.JSONDecodeError as e:
        logging.error(f"JSON inválido en {nombre_archivo}: {e}")
    except Exception as e:
        logging.exception(f"Error al leer el JSON: {e}")

    return lista_usuarios
