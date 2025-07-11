from input_utils import *

def obtener_opcion_numero(opciones:str, mensaje:str, mensaje_error:str) -> int:
    ingreso_usuario = input(mensaje)
    while not verificar_caracter_en_cadena(ingreso_usuario, opciones):
        ingreso_usuario = input(mensaje_error)
    ingreso_usuario = int(ingreso_usuario)
    return ingreso_usuario

def obtener_opcion_letra(opciones:str, mensaje:str, mensaje_error:str) -> str:
    ingreso_usuario = input(mensaje)
    while not verificar_caracter_en_cadena(ingreso_usuario, opciones):
        ingreso_usuario = input(mensaje_error)
    return ingreso_usuario

def obtener_cadena(mensaje:str, mensaje_error:str, caracteres_posibles:str = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_1234567890!@#$%") -> str:
    ingreso = input(mensaje)
    while not verificar_cadena(ingreso, caracteres_posibles):
        ingreso = input(mensaje_error)
    return ingreso
    
