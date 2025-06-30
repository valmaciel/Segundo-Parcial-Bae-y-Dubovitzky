import random
from especificas import *
from input import *

def main():
    print('😂😂😂😂😂😂😂😂😂😂😂¡Bienvenidos a Preguntados!😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂')

    preguntas_por_categoria = {
    "Historia": [
        {"pregunta": "¿Quién fue el primer presidente de Argentina?", "opciones": ["Rivadavia", "San Martín", "Belgrano", "Sarmiento"], "respuesta": "a", "categoria": "Historia"},
        {"pregunta": "¿En qué año comenzó la Revolución Francesa?", "opciones": ["1789", "1776", "1804", "1799"], "respuesta": "a", "categoria": "Historia"},
        {"pregunta": "¿Qué civilización construyó las pirámides?", "opciones": ["Romana", "Egipcia", "Griega", "Maya"], "respuesta": "b", "categoria": "Historia"},
        {"pregunta": "¿Quién fue Napoleón Bonaparte?", "opciones": ["Un filósofo", "Un emperador francés", "Un rey inglés", "Un científico"], "respuesta": "b", "categoria": "Historia"},
        {"pregunta": "¿Qué país inició la Segunda Guerra Mundial?", "opciones": ["Italia", "Japón", "Alemania", "Rusia"], "respuesta": "c", "categoria": "Historia"}
    ],
    "Ciencia": [
        {"pregunta": "¿Cuál es la fórmula del agua?", "opciones": ["H2O", "CO2", "NaCl", "O2"], "respuesta": "a", "categoria": "Ciencia"},
        {"pregunta": "¿Qué planeta es el más cercano al Sol?", "opciones": ["Venus", "Marte", "Mercurio", "Tierra"], "respuesta": "c", "categoria": "Ciencia"},
        {"pregunta": "¿Qué gas respiramos principalmente?", "opciones": ["Oxígeno", "Nitrógeno", "Dióxido de carbono", "Hidrógeno"], "respuesta": "b", "categoria": "Ciencia"},
        {"pregunta": "¿Cuántos huesos tiene el cuerpo humano adulto?", "opciones": ["206", "208", "210", "215"], "respuesta": "a", "categoria": "Ciencia"},
        {"pregunta": "¿Qué científico desarrolló la teoría de la relatividad?", "opciones": ["Einstein", "Newton", "Galileo", "Tesla"], "respuesta": "a", "categoria": "Ciencia"}
    ],
    "Geografía": [
        {"pregunta": "¿Cuál es la capital de Japón?", "opciones": ["Kioto", "Osaka", "Tokio", "Hiroshima"], "respuesta": "c", "categoria": "Geografía"},
        {"pregunta": "¿Dónde queda el monte Everest?", "opciones": ["India", "Nepal", "China", "Tíbet"], "respuesta": "b", "categoria": "Geografía"},
        {"pregunta": "¿Cuál es el río más largo del mundo?", "opciones": ["Amazonas", "Nilo", "Yangtsé", "Misisipi"], "respuesta": "a", "categoria": "Geografía"},
        {"pregunta": "¿Qué país tiene forma de bota?", "opciones": ["Grecia", "España", "Italia", "Portugal"], "respuesta": "c", "categoria": "Geografía"},
        {"pregunta": "¿En qué continente está Egipto?", "opciones": ["Asia", "Europa", "África", "Oceanía"], "respuesta": "c", "categoria": "Geografía"}
    ],
    "Arte": [
        {"pregunta": "¿Quién pintó la Mona Lisa?", "opciones": ["Picasso", "Van Gogh", "Da Vinci", "Dalí"], "respuesta": "c", "categoria": "Arte"},
        {"pregunta": "¿Qué instrumento usaba Beethoven?", "opciones": ["Violín", "Flauta", "Piano", "Guitarra"], "respuesta": "c", "categoria": "Arte"},
        {"pregunta": "¿Cuál es un estilo artístico?", "opciones": ["Realismo", "Física", "Geografía", "Matemática"], "respuesta": "a", "categoria": "Arte"},
        {"pregunta": "¿Qué escultor hizo 'El David'?", "opciones": ["Donatello", "Da Vinci", "Miguel Ángel", "Raphael"], "respuesta": "c", "categoria": "Arte"},
        {"pregunta": "¿Qué movimiento es Dalí?", "opciones": ["Cubismo", "Surrealismo", "Impresionismo", "Barroco"], "respuesta": "b", "categoria": "Arte"}
    ],
    "Deportes": [
        {"pregunta": "¿En qué deporte se usa una raqueta?", "opciones": ["Fútbol", "Tenis", "Boxeo", "Hockey"], "respuesta": "b", "categoria": "Deportes"},
        {"pregunta": "¿Cuántos jugadores tiene un equipo de fútbol?", "opciones": ["9", "10", "11", "12"], "respuesta": "c", "categoria": "Deportes"},
        {"pregunta": "¿Dónde se juegan los Juegos Olímpicos?", "opciones": ["Un solo país", "Cada continente", "Cada 4 años en diferentes países", "Siempre en Grecia"], "respuesta": "c", "categoria": "Deportes"},
        {"pregunta": "¿Qué deporte practica Lionel Messi?", "opciones": ["Tenis", "Fútbol", "Básquet", "Golf"], "respuesta": "b", "categoria": "Deportes"},
        {"pregunta": "¿Cuál es un deporte de invierno?", "opciones": ["Snowboard", "Fútbol", "Ciclismo", "Atletismo"], "respuesta": "a", "categoria": "Deportes"}
    ],
    "Entretenimiento": [
        {"pregunta": "¿Quién protagoniza 'Iron Man'?", "opciones": ["Chris Evans", "Robert Downey Jr.", "Mark Ruffalo", "Tom Holland"], "respuesta": "b", "categoria": "Entretenimiento"},
        {"pregunta": "¿Cuál es la casa de Harry Potter?", "opciones": ["Ravenclaw", "Slytherin", "Hufflepuff", "Gryffindor"], "respuesta": "d", "categoria": "Entretenimiento"},
        {"pregunta": "¿Qué serie es conocida por los dragones?", "opciones": ["Breaking Bad", "Friends", "Game of Thrones", "Stranger Things"], "respuesta": "c", "categoria": "Entretenimiento"},
        {"pregunta": "¿Quién canta 'Shape of You'?", "opciones": ["Ed Sheeran", "Justin Bieber", "Shawn Mendes", "Bruno Mars"], "respuesta": "a", "categoria": "Entretenimiento"},
        {"pregunta": "¿Qué superhéroe es conocido como el 'Caballero de la Noche'?", "opciones": ["Superman", "Iron Man", "Batman", "Spider-Man"], "respuesta": "c", "categoria": "Entretenimiento"}
    ]
}


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
