from especificas_simples import *
from input import *
from generales import *
from parser import *
from usuarios import *
import time
import os

def jugar_pregunta(jugador, preguntas_dict, categoria_electa, bandera_ronda_corona = False):
    print(f'🎯 Turno de: {jugador['nombre']}\n')
    terminado = False
    pregunta_numero = elegir_numero_de_pregunta_aleatorio(preguntas_dict, categoria_electa)
    pregunta_de_ronda = preguntas_dict[categoria_electa][pregunta_numero]
    hacer_pregunta(categoria_electa, pregunta_de_ronda['pregunta'], pregunta_de_ronda['opciones'])
    inicio = time.time()
    ingreso = obtener_respuesta(['a','b','c','d'])
    final = time.time()
    tiempo = calcular_tiempo(inicio, final)
    mandar_tiempo(tiempo, jugador)
    if verificar_respuesta(pregunta_de_ronda['respuesta'], ingreso):
        print('✅ ¡Correcto!')
        agregar_acierto_o_error(jugador['nombre'], jugador['contra'])
        if bandera_ronda_corona:
            jugador['puntos_corona'] = 0
            jugador['puntos'] += 1
        else:
            jugador['puntos_corona'] += 1
    else:
        agregar_acierto_o_error(jugador['nombre'], jugador['contra'], acierto=False)
        print(f'❌ Incorrecto. Respuesta correcta: {pregunta_de_ronda['respuesta']}\n Fin del turno.\n')
        jugador['puntos_corona'] = 0
        terminado = True
    time.sleep(3)
    os.system("cls")
    return terminado

def jugar_ronda_corona(jugador, categorias_por_letra, preguntas_dict, categorias):
    print(f'¡Te ha tocado la categoría de corona!\nElige de las siguientes opciones:')
    for i in range(len(categorias) - 1):
        print(f'{chr(97 + i)}) {categorias[i]}')
    categoria_electa_por_jugador = obtener_respuesta(['a','b','c','d','e','f'])
    os.system("cls")
    categoria_electa = convertir_respuesta_a_categoria(categoria_electa_por_jugador, categorias_por_letra)
    categoria_electa = verificar_categoria_restante(jugador, categorias_por_letra, categoria_electa)
    jugador['categorias_restantes'].remove(categoria_electa)
    terminado = jugar_pregunta(jugador, preguntas_dict, categoria_electa, bandera_ronda_corona = True)
    return terminado

def jugar_turno(jugadorid:int , categorias:list, preguntas_dict:dict, categorias_por_letra:dict, jugadores:dict) -> bool:
    terminado = False
    jugador = jugadores['jugadores'][jugadorid]
    while not terminado:
        if jugador['puntos'] >= 1:
            break
        print(f'Puntos de corona: {jugador['puntos_corona']}\n')
        categoria_electa = obtener_categoria_aleatoria(categorias)
        if calcular_puntos_coronas(categoria_electa, jugador['puntos_corona']):
            terminado = jugar_ronda_corona(jugador, categorias_por_letra, preguntas_dict, categorias)
        else:
            terminado = jugar_pregunta(jugador, preguntas_dict, categoria_electa)
    cargar_datos_json(jugadores)
    return terminado

def jugar_juego(usuario1, contra1):
    preguntas_por_categoria = parser_csv()

    categorias = ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento', 'Corona']

    categorias_por_letra = {'a': 'Historia',
                            'b': 'Ciencia',
                            'c': 'Geografía',
                            'd': 'Arte',
                            'e': 'Deportes',
                            'f': 'Entretenimiento'}
    
    jugadores = parser_json()
    lista_usuarios = jugadores["jugadores"]
    jugadorid_1 = obtener_id_usuario(usuario1, contra1)
    os.system("cls")
    print("Por favor ingresar datos del segundo jugador")
    usuario2, contra2 = loguear_usuario(lista_usuarios)
    jugadorid_2 = obtener_id_usuario(usuario2, contra2)
    os.system("cls")

    jugador1 = jugadores['jugadores'][jugadorid_1]
    jugador2 = jugadores['jugadores'][jugadorid_2]

    turno_jugador = True
    en_juego = True
    puntos_necesarios = 1
    
    while en_juego:
        while turno_jugador:
            while jugador1['puntos'] >= puntos_necesarios or jugador2['puntos'] >= puntos_necesarios:
                en_juego = False
                break
            turno_jugador = jugar_turno(jugadorid_1, categorias, preguntas_por_categoria, categorias_por_letra, jugadores)
            turno_jugador = False
        while not turno_jugador:
            while jugador1['puntos'] >= puntos_necesarios or jugador2['puntos'] >= puntos_necesarios:
                en_juego = False
                break
            turno_jugador = jugar_turno(jugadorid_2, categorias, preguntas_por_categoria, categorias_por_letra, jugadores)
            turno_jugador = True

    os.system("cls")
    
    if jugador1['puntos'] > jugador2['puntos']:
        jugador1['wins'] += 1
        print(f'🎉 Ganador: {jugador1["nombre"]}')
    elif jugador2['puntos'] > jugador1['puntos']:
        jugador2['wins'] += 1
        print(f'🎉 Ganador: {jugador2["nombre"]}')
    else:
        print('Empate!')

    jugador1['puntos'] = 0
    jugador2['puntos'] = 0

    agregar_todas_las_categorias()

    cargar_datos_json(jugadores)

    print("\n🎉 Fin del juego. Gracias por jugar Preguntados!")
    input('Presiona ENTER para salir')

def ingreso_a_menu_principal(usuario, password):
    bandera_salir = True
    while bandera_salir:
        os.system('cls')
        print(f'Bienvenido {usuario}\n')
        print('''¿Qué desea hacer?

    1. Jugar partida
    2. Cambiar aspecto
    3. Ajustes
    4. Ver estadísticas globales
    5. Cerrar sesión
            ''')
        
        ingreso_usuario = manejar_menu("12345")

        if ingreso_usuario == 1:
            jugar_juego(usuario, password)
        elif ingreso_usuario == 2:
            cambiar_aspecto(usuario, password)
        elif ingreso_usuario == 3:
            pass
        elif ingreso_usuario == 4:
            mostrar_estadisticas()
        elif ingreso_usuario == 5:
            bandera_salir = False
            break

