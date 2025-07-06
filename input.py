from generales import *

def obtener_respuesta(lista_respuestas_permitidas):
    ingreso = input('Ingrese su respuesta: ').lower()
    while not buscar_variable_en_lista(ingreso, lista_respuestas_permitidas):
        ingreso = input('❗Respuesta inválida...\nIngrese su respuesta: ').lower()
    return ingreso

def manejar_menu(opciones_posibles:str):
    ingreso_usuario = input("Ingrese su opción: ")
    while not verificar_input_en_string(ingreso_usuario, string_con_caracteres_posibles = opciones_posibles):
        ingreso_usuario = input("Error de lectura... ingrese su opción: ")
    ingreso_usuario = int(ingreso_usuario)
    return ingreso_usuario 

def obtener_respuesta_1(caracteres_posibles:str, mensaje = 'Ingrese su opción: ', mensaje_error = 'Error de lectura, ingrese su opción: '):
    ingreso = input(mensaje)
    while not verificar_input_en_string(ingreso, caracteres_posibles):
        ingreso = input(mensaje_error)
    ingreso = int(ingreso)
    return ingreso
        
