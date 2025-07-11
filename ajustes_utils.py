from parser import *
from input import *

def toggle_booleano_json(configuracion:str, subconfiguracion:str, toggle:bool):
    archivo_config = leer_archivo_json("configfiles/config.json")
    archivo_config[configuracion][subconfiguracion] = toggle
    escribir_archivo_json(archivo_config, "configfiles/config.json")

def cambiar_opcion_daltonismo(tipo_daltonismo:str):
    tipos_validos_daltonismo = ["ninguno", "protanopia", "deuteranopia", "tritanopia"]
    bandera_valido = False
    for i in range(len(tipos_validos_daltonismo)):
        if tipo_daltonismo == tipos_validos_daltonismo[i]:
            bandera_valido = True
            break
    if bandera_valido:
        archivo_config = leer_archivo_json("configfiles/config.json")
        archivo_config["accesibilidad"]["daltonismo"] = tipo_daltonismo
        escribir_archivo_json(archivo_config, "configfiles/config.json")

def cambiar_opcion_sonido(subconfiguracion:str, numero_de_volumen:int):
    archivo_config = leer_archivo_json("configfiles/config.json")
    archivo_config["volumen"][subconfiguracion] = numero_de_volumen
    escribir_archivo_json(archivo_config, "configfiles/config.json")

def obtener_numero_0_al_100():
    numero = obtener_cadena("Ingrese volumen deseado (0-100): ", "Error de lectura, ingrese volumen deseado (0-100): ", "1234567890")
    while not (0 <= int(numero) <= 100):
        print("Error: Fuera de rango.")
        numero = obtener_cadena("Ingrese volumen deseado (0-100): ", "Error de lectura, ingrese volumen deseado (0-100): ", "1234567890")
    numero = int(numero)
    return numero