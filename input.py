from generales import *

def obtener_respuesta(lista_respuestas_permitidas):
    ingreso = input('Ingrese su respuesta: ').lower()
    while not buscar_variable_en_lista(ingreso, lista_respuestas_permitidas):
        ingreso = input('❗Respuesta inválida...\nIngrese su respuesta: ').lower()
    return ingreso