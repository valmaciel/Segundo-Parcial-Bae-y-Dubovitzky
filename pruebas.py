from especificas import *

jugador1 = {
    "nombre": "Denis",
    "puntos": 0,
    "puntos_corona": 0,
    "categorias_restantes": ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento']
}


preguntas_por_categoria = {
        "Historia": [
            {"pregunta": "¿Quién fue el primer presidente de Argentina?", "opciones": ["Rivadavia", "San Martín", "Belgrano", "Sarmiento"], "respuesta": "a", "categoria": "Historia"},
        ],
        "Ciencia": [
            {"pregunta": "¿Cuál es la fórmula del agua?", "opciones": ["H2O", "CO2", "NaCl", "O2"], "respuesta": "a", "categoria": "Ciencia"},
        ],
        "Geografía": [
            {"pregunta": "¿Cuál es la capital de Japón?", "opciones": ["Kioto", "Osaka", "Tokio", "Hiroshima"], "respuesta": "c", "categoria": "Geografía"},
        ],
        "Arte": [
            {"pregunta": "¿Quién pintó la Mona Lisa?", "opciones": ["Picasso", "Van Gogh", "Da Vinci", "Dalí"], "respuesta": "c", "categoria": "Arte"},
        ],
        "Deportes": [
            {"pregunta": "¿En qué deporte se usa una raqueta?", "opciones": ["Fútbol", "Tenis", "Boxeo", "Hockey"], "respuesta": "b", "categoria": "Deportes"},
        ],
        "Entretenimiento": [
            {"pregunta": "¿Quién protagoniza 'Iron Man'?", "opciones": ["Chris Evans", "Robert Downey Jr.", "Mark Ruffalo", "Tom Holland"], "respuesta": "b", "categoria": "Entretenimiento"},
        ]
    }

categorias = ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento', 'Corona']

categorias_por_letra = {'a': 'Historia',
                        'b': 'Ciencia',
                        'c': 'Geografía',
                        'd': 'Arte',
                        'e': 'Deportes',
                        'f': 'Entretenimiento'}

# categoria_random = obtener_categoria_aleatoria(categorias)

# print(categoria_random)

# print(hacer_pregunta(categoria_random, preguntas_por_categoria[categoria_random][0]['pregunta'], preguntas_por_categoria[categoria_random][0]['opciones']))

# ingreso = obtener_respuesta(['a','b','c','d'])

# if verificar_respuesta(preguntas_por_categoria[categoria_random][0]['respuesta'], ingreso):
#     print('correcto')
# else:
#     print('incorrecto')

puntos_jugador_1 = 0
categorias_restantes_jugador_1 = ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento']

for i in range(6):
    jugar_turno(jugador1, categorias, preguntas_por_categoria, categorias_por_letra)
    print(jugador1['puntos'])