import random
from especificas import *
from input import *
from parser import *

def main():
    print('\n¡Bienvenidos a Preguntados!\n')

    preguntas_por_categoria = parser_csv()

    categorias = ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento', 'Corona']

    categorias_por_letra = {'a': 'Historia',
                            'b': 'Ciencia',
                            'c': 'Geografía',
                            'd': 'Arte',
                            'e': 'Deportes',
                            'f': 'Entretenimiento'}
    
    jugador1 = {"nombre": "Denis",
                "puntos": 0,
                "puntos_corona": 0,
                "categorias_restantes": ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento']}
    
    jugador2 = {"nombre": "Valentina",
                "puntos": 0,
                "puntos_corona": 0,
                "categorias_restantes": ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento']}
    
    turno_jugador = True
    en_juego = True
    
    while en_juego:
        while turno_jugador:
            if jugador1['puntos'] >= 6 or jugador2['puntos'] >= 6:
                en_juego = False
            turno_jugador = jugar_turno(jugador1, categorias, preguntas_por_categoria, categorias_por_letra)
            turno_jugador = False
        while not turno_jugador:
            if jugador1['puntos'] >= 6 or jugador2['puntos'] >= 6:
                en_juego = False
            turno_jugador = jugar_turno(jugador2, categorias, preguntas_por_categoria, categorias_por_letra)
            turno_jugador = True
    
    if jugador1['puntos'] > jugador2['puntos']:
        print(f'🎉 Ganador: {jugador1["nombre"]}')
    elif jugador2['puntos'] > jugador1['puntos']:
        print(f'🎉 Ganador: {jugador2["nombre"]}')
    else:
        print('Empate!')

    print("\n🎉 Fin del juego. Gracias por jugar Preguntados!")

if __name__ == "__main__":
    main()
