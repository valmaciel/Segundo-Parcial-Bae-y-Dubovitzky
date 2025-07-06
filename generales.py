def buscar_variable_en_lista(variable, lista):
    bandera = False
    for i in range(len(lista)):
        if variable == lista[i]:
            bandera = True
    return bandera

def verificar_respuesta(valor_correcto, ingreso):
    bandera_correcto = False
    if valor_correcto == ingreso:
        bandera_correcto = True
    return bandera_correcto

def verificar_input_en_string(entrada, string_con_caracteres_posibles):
    bandera = False
    for i in range(len(string_con_caracteres_posibles)):
        if entrada == string_con_caracteres_posibles[i]:
            bandera = True
    return bandera

def calcular_tiempo(inicio, final):
    tiempo = final - inicio
    return tiempo   