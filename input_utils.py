def verificar_cadenas_iguales(cadena1:str, cadena2:str) -> bool:
    if cadena1 == cadena2:
        bandera = True
    else:
        bandera = False
    return bandera

def verificar_cadena(ingreso: str, caracteres_posibles: str = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_1234567890!@#$%") -> bool:
    bandera_valido = True
    for i in range(len(ingreso)):
        bandera_encontrado = False
        for j in range(len(caracteres_posibles)):
            if ingreso[i] == caracteres_posibles[j]:
                bandera_encontrado = True
                break
        if not bandera_encontrado:
            bandera_valido = False
            break
    return bandera_valido

def verificar_caracter_en_cadena(caracter:str, cadena:str) -> bool:
    bandera = False
    for i in range(len(cadena)):
        if caracter == cadena[i]:
            bandera = True
    return bandera

def verificar_caracter_en_lista(caracter:str, lista:list) -> bool:
    bandera = False
    for i in range(len(lista)):
        if caracter == lista[i]:
            bandera = True
    return bandera

def obtener_cadena_de_numeros(n):
    cadena = ""
    for i in range(1, n + 1):
        cadena += (str(i))
    return cadena