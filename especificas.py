import random

def obtener_categoria_aleatoria(lista_categorias):
    categoria_elegida = random.choice(lista_categorias)
    return categoria_elegida

def hacer_pregunta(categoria:str, pregunta:str, opciones:list):
    print(f'Categoría: {categoria}')
    print(pregunta)
    for i in range(len(opciones)):
        print(f'{chr(97 + i)}) {opciones[i]}')

def buscar_variable_en_lista(variable, lista):
    bandera = False
    for i in range(len(lista)):
        if variable == lista[i]:
            bandera = True
    return bandera

def obtener_respuesta(lista_respuestas_permitidas):
    ingreso = input('Ingrese su respuesta: ').lower()
    while not buscar_variable_en_lista(ingreso, lista_respuestas_permitidas):
        ingreso = input('❗Respuesta inválida...\nIngrese su respuesta: ').lower()
    return ingreso

def verificar_respuesta(valor_correcto, ingreso):
    bandera_correcto = False
    if valor_correcto == ingreso:
        bandera_correcto = True
    return bandera_correcto

def calcular_puntos_coronas(categoria_electa, puntos_corona):
    bandera_ronda_corona = False
    if categoria_electa == 'Corona' or puntos_corona >= 3:
        bandera_ronda_corona = True
    return bandera_ronda_corona

def convertir_respuesta_a_categoria(ingreso:str, diccionario_mapeo_categorias:dict):
    categoria_en_string = diccionario_mapeo_categorias[ingreso]
    return categoria_en_string

def elegir_numero_de_pregunta_aleatorio(diccionario_con_preguntas:dict, categoria:str):
    cantidad_preguntas = len(diccionario_con_preguntas[categoria])
    numero_de_pregunta_random = random.randint(0, cantidad_preguntas - 1)
    return numero_de_pregunta_random

def jugar_turno(jugador:dict , categorias:list, preguntas_dict:dict, categorias_por_letra:dict, ):
    while True:
        print(f'\n🎯 Turno de: {jugador['nombre']}')
        print(f'Puntos de corona: {jugador['puntos_corona']}')
        categoria_electa = obtener_categoria_aleatoria(categorias)
        if calcular_puntos_coronas(categoria_electa, jugador['puntos_corona']):
            print(f'¡Te ha tocado la categoría de corona!\nElige de las siguientes opciones:')
            for i in range(len(categorias) - 1):
                print(f'{chr(97 + i)}) {categorias[i]}')
            categoria_electa_por_jugador = obtener_respuesta(['a','b','c','d','e','f'])
            categoria_electa = convertir_respuesta_a_categoria(categoria_electa_por_jugador, categorias_por_letra)
            while not buscar_variable_en_lista(categoria_electa, jugador['categorias_restantes']):
                print(f'Error... Ya tienes la corona de esa categoría\nCategorías restantes: {jugador['categorias_restantes']}')
                categoria_electa_por_jugador = obtener_respuesta(['a','b','c','d','e','f'])
                categoria_electa = convertir_respuesta_a_categoria(categoria_electa_por_jugador, categorias_por_letra)
            jugador['categorias_restantes'].remove(categoria_electa)
            pregunta_numero = elegir_numero_de_pregunta_aleatorio(preguntas_dict, categoria_electa)
            pregunta_de_ronda = preguntas_dict[categoria_electa][pregunta_numero]
            hacer_pregunta(categoria_electa, pregunta_de_ronda['pregunta'], pregunta_de_ronda['opciones'])
            ingreso = obtener_respuesta(['a','b','c','d'])
            if verificar_respuesta(pregunta_de_ronda['respuesta'], ingreso):
                print('✅ ¡Correcto!')
                jugador['puntos_corona'] = 0
                jugador['puntos'] += 1
            else:
                print(f'❌ Incorrecto. Respuesta correcta: {pregunta_de_ronda['respuesta']}\n Fin del turno.\n')
                jugador['puntos_corona'] = 0
                break        
        else:
            pregunta_numero = elegir_numero_de_pregunta_aleatorio(preguntas_dict, categoria_electa)
            pregunta_de_ronda = preguntas_dict[categoria_electa][pregunta_numero]
            hacer_pregunta(categoria_electa, pregunta_de_ronda['pregunta'], pregunta_de_ronda['opciones'])
            ingreso = obtener_respuesta(['a','b','c','d'])
            if verificar_respuesta(pregunta_de_ronda['respuesta'], ingreso):
                print('✅ ¡Correcto!')
                jugador['puntos_corona'] += 1
            else:
                print(f'❌ Incorrecto. Respuesta correcta: {pregunta_de_ronda['respuesta']}\n Fin del turno.\n')
                break