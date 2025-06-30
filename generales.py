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